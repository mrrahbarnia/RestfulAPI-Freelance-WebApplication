from django.core.validators import MinLengthValidator
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import (
    serializers,
    permissions
)
from drf_spectacular.utils import extend_schema

from core.pagination import (
    LimitOffsetPagination,
    get_paginated_response_context
)
from core.selectors.users import (
    get_profile,
    get_freelancers
)
from core.services.users import (
    register,
    update_profile,
    profile_detail,
    subscribe,
    unsubscribe
)
from .models import (
    BaseUser,
    Profile
)
from .validators import (
    phone_validator,
    letter_validator,
    number_validator,
    special_character_validator
)


class RegistrationApiView(APIView):


    class InputRegisterSerializer(serializers.Serializer):
        phone_number = serializers.CharField(
            validators = [phone_validator]
        )
        email = serializers.EmailField(required=False)
        password = serializers.CharField(
            validators=[
                MinLengthValidator(limit_value=8),
                number_validator,
                letter_validator,
                special_character_validator
            ]
        )
        confirm_password = serializers.CharField(write_only=True)

        def validate_phone_number(self, phone_number):
            """Validating phone number to be unique."""
            if BaseUser.objects.filter(
                phone_number=phone_number
            ).exists():
                raise APIException(
                    'The provided phone number has already been taken.'
                )
            return phone_number

        def validate(self, attrs):
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            if password != confirm_password:
                raise APIException(
                    'Passwords must be match.'
                )

            return attrs


    class OutputRegisterSerializer(serializers.ModelSerializer):

        class Meta:
            model = BaseUser
            fields = ('phone_number', 'created_at')

    @extend_schema(
            request=InputRegisterSerializer,
            responses=OutputRegisterSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            logic = register(
                phone_number=serializer.validated_data.get('phone_number'),
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password')
            )
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )

        response = self.OutputRegisterSerializer(logic).data
        return Response(response, status=status.HTTP_200_OK)


class ProfileMeApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    class UpdateProfileSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        bio = serializers.CharField(max_length=1000, required=False)
        image = serializers.ImageField(required=False)
        age = serializers.IntegerField(required=False)
        sex = serializers.CharField(max_length=1, required=False)
        city = serializers.CharField(max_length=100, required=False)

        def validate_sex(self, sex):
            if sex != 'M' and sex != 'F':
                raise APIException(
                    "Sex must be exactly either 'M' or 'F' string."
                )
            return sex

        def validate_age(self, age):
            if age < 1:
                raise APIException(
                    'Age must be a positive digit.'
                )
            return age


    class OutPutProfileMeSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Profile
            fields = (
                'email', 'bio', 'image', 'age', 'plan_type',
                'balance', 'score', 'sex', 'city', 'views'
            )

    @extend_schema(responses=OutPutProfileMeSerializer)
    def get(self, request, *args, **kwargs):
        try:
            profile = get_profile(user=request.user)
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )
        response = self.OutPutProfileMeSerializer(profile).data

        return Response(response, status=status.HTTP_200_OK)
    
    @extend_schema(
            request=UpdateProfileSerializer,
            responses=OutPutProfileMeSerializer
    )
    def patch(self, request, *args, **kwargs):
        serializer = self.UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            profile = update_profile(
                user=request.user,
                email=serializer.validated_data.get('email'),
                bio=serializer.validated_data.get('bio'),
                image=serializer.validated_data.get('image'),
                age=serializer.validated_data.get('age'),
                sex=serializer.validated_data.get('sex'),
                city=serializer.validated_data.get('city')
            )
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )

        response = self.OutPutProfileMeSerializer(profile).data
        return Response(response, status=status.HTTP_200_OK)


class ProfileDetailApiView(APIView):


    class OutputProfileDetailSerializer(serializers.ModelSerializer):

        class Meta:
            model = Profile
            fields = (
                'email', 'bio', 'image', 'age', 'plan_type',
                'score', 'sex', 'city', 'views'
            )

    @extend_schema(
            responses=OutputProfileDetailSerializer
    )
    def get(self, request, uuid, *args, **kwargs):
        try:
            profile = profile_detail(uuid=uuid)
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )

        response = self.OutputProfileDetailSerializer(profile).data
        return Response(response, status=status.HTTP_200_OK)


class SubscriptionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, uuid, *args, **kwargs):
        try:
            subscribe(
                follower=request.user.profile, target_uuid=uuid
            )
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, uuid, *args, **kwargs):
        try:
            unsubscribe(
                un_follower=request.user.profile, target_uuid=uuid
            )
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFreelancersApiView(APIView):


    class Pagination(LimitOffsetPagination):
        default_limit = 20


    class OutputFreelancersSerializer(serializers.ModelSerializer):
        absolute_url = serializers.SerializerMethodField()
        class Meta:
            model = Profile
            fields = (
                'email', 'bio', 'image',
                'score', 'absolute_url'
            )

        def get_absolute_url(self, profile):
            request = self.context.get('request')
            path = reverse('users:profile_detail', args=[profile.uuid])
            return request.build_absolute_uri(path)

    @extend_schema(responses=OutputFreelancersSerializer)
    def get(self, request, *args, **kwargs):
        try:
            freelancers = get_freelancers()
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutputFreelancersSerializer,
            queryset=freelancers,
            request=request,
            view=self
        )
