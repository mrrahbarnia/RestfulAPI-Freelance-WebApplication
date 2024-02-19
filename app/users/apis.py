from django.core.validators import MinLengthValidator
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import (
    serializers,
    permissions
)
from drf_spectacular.utils import extend_schema

from core.selectors.users import (
    get_profile
)
from core.services.users import (
    register
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


    class OutPutProfileMeSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Profile
            fields = (
                'email', 'bio', 'image', 'age', 'plan_type',
                'balance', 'score', 'sex', 'city', 'views'
            )

    def get(self, request, *args, **kwargs):
        try:
            profile = get_profile(user=request.user)
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )
        response = self.OutPutProfileMeSerializer(profile).data

        return Response(response, status=status.HTTP_200_OK)
