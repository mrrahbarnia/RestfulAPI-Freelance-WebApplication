import logging

from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import (
    status,
    serializers
)

from core.selectors.skills import (
    get_categories,
    get_skills
)
from core.services.skills import (
    create_category,
    create_skill
)
from .models import (
    Skill,
    Category
)
from .permission import IsAdminOrReadOnly

logger = logging.getLogger(__name__)


class CategoryApiView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    class InputCategorySerializer(serializers.Serializer):
        name = serializers.CharField(max_length=250, required=True)

        def validate_name(self, name):
            if Category.objects.filter(name=name).exists():
                raise serializers.ValidationError(
                    'There is a category with the same name.'
                )


    class OutputCategorySerializer(serializers.ModelSerializer):

        class Meta:
            model = Skill
            fields = ('name',)

    @extend_schema(responses=OutputCategorySerializer)
    def get(self, request, *args, **kwargs):
        try:
            categories = get_categories(name=None)
        except Exception as ex:
            logger.warning(f'Database Error >> {ex}')
            raise APIException(f'Database Error >> {ex}')
        response = self.OutputCategorySerializer(categories, many=True).data

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
            logger.warning(f'Database Error >> {ex}')
            raise APIException(f'Database Error >> {ex}')
        response = self.OutputCategorySerializer(category).data

        return Response(response, status=status.HTTP_201_CREATED)


class SkillApiView(APIView):
    permission_classes = [IsAdminOrReadOnly]


    class InputSkillSerializer(serializers.Serializer):

        CATEGORIES = get_categories(name=None)
        CATEGORY_CHOICES = [category.name for category in CATEGORIES]

        name = serializers.CharField(max_length=250)
        category = serializers.ChoiceField(
            choices=CATEGORY_CHOICES,
            help_text=f'The category name must be in this list >> {CATEGORY_CHOICES}'
        )

        def validate_name(self, name):
            if Skill.objects.filter(name=name).exists():
                raise serializers.ValidationError(
                    'There is a skill with the same name.'
                )
            return name


    class OutputSkillSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Skill
            fields = ('name', )

    @extend_schema(responses=OutputSkillSerializer)
    def get(self, request, *args, **kwargs):
        try:
            skills = get_skills(category=None)
        except Exception as ex:
            logger.warning(f'Database Error >> {ex}')
            raise APIException(f'Database Error >> {ex}')
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
            category = get_categories(
                name=serializer.validated_data.get('category')
            )
            skill = create_skill(
                name=serializer.validated_data.get('name'),
                category=category
            )
        except Exception as ex:
            logger.warning(f'Database Error >> {ex}')
            raise APIException(f'Database Error >> {ex}')
        response = self.OutputSkillSerializer(skill).data
        return Response(response, status=status.HTTP_201_CREATED)