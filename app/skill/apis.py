from django.urls import reverse
from rest_framework import (
    status,
    serializers
)
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from core.selectors.skills import (
    get_published_categories,
    get_published_skills,
    category_choices
)
from core.services.skills import (
    create_category,
    create_skill,
    publish_category,
    publish_skill
)
from .models import (
    Skill,
    Category
)
from .permission import (
    IsAdminOrReadOnly,
    IsAdmin
)


class CategoryApiView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    class InputCategorySerializer(serializers.Serializer):
        name = serializers.CharField(max_length=250, required=True)

        def validate_name(self, name):
            if Category.objects.filter(name=name).exists():
                raise serializers.ValidationError(
                    'There is a category with the provided name.'
                )
            return name


    class OutputCategorySerializer(serializers.ModelSerializer):
        # publish_url = serializers.SerializerMethodField()

        class Meta:
            model = Category
            fields = ('name', )

        # def get_publish_url(self, category):
        #     request = self.context.get('request')
        #     path = reverse('skill:category_detail', args=[category.slug])
        #     return request.build_absolute_uri(path)


    @extend_schema(responses=OutputCategorySerializer)
    def get(self, request, *args, **kwargs):
        try:
            categories = get_published_categories(name=None)
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )
        response = self.OutputCategorySerializer(categories, many=True, context={'request': request}).data

        return Response(response, status=status.HTTP_200_OK)

    @extend_schema(
            request=InputCategorySerializer,
            responses=OutputCategorySerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            category = create_category(
                name=serializer.validated_data.get('name')
            )
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )
        response = self.OutputCategorySerializer(category).data

        return Response(response, status=status.HTTP_201_CREATED)




class SkillApiView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    class InputSkillSerializer(serializers.Serializer):

        CATEGORY_CHOICES = category_choices()

        name = serializers.CharField(max_length=250)
        category = serializers.ChoiceField(
            choices=CATEGORY_CHOICES,
            help_text=f'The category name must be in this list >> {CATEGORY_CHOICES}'
        )

        def validate_name(self, name):
            if Skill.objects.filter(name=name).exists():
                raise serializers.ValidationError(
                    'There is a skill with the same name'
                )
            return name


    class OutputSkillSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Skill
            fields = ('name', )

    @extend_schema(responses=OutputSkillSerializer)
    def get(self, request, *args, **kwargs):
        try:
            skills = get_published_skills(category=None)
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )
        response = self.OutputSkillSerializer(skills, many=True).data
        return Response(response, status=status.HTTP_200_OK)

    @extend_schema(
            request=InputSkillSerializer,
            responses=OutputSkillSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputSkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            category = get_published_categories(
                name=serializer.validated_data.get('category')
            )
            skill = create_skill(
                name=serializer.validated_data.get('name'),
                category=category
            )
        except Exception as ex:
            raise APIException(
                f'Database Error >> {ex}'
            )
        response = self.OutputSkillSerializer(skill).data
        return Response(response, status=status.HTTP_201_CREATED)


class CategoryDetailApiView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, slug=None, *args, **kwargs):
        try:
            publish_category(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                f'Database Error >> {ex}'
            )
        return Response(status=status.HTTP_200_OK)


class SkillDetailApiView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, slug=None, *args, **kwargs):
        try:
            publish_skill(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                f'Database Error >> {ex}'
            )
        return Response(status=status.HTTP_200_OK)
