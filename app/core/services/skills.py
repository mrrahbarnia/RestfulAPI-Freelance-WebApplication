from django.utils.text import slugify
from django.core.exceptions import ValidationError
from rest_framework import serializers

from skill.models import (
    Skill,
    Category
)

def create_category(*, name:str) -> Category:
    return Category.objects.create(name=name, slug=slugify(name))

def create_skill(*, name:str, category:Category) -> Skill:
    return Skill.objects.create(name=name, category=category, slug=slugify(name))

def publish_category(*, slug:str) -> None:
    try:
        category = Category.objects.get(slug=slug)
        category.status = True
        category.save()
    except Category.DoesNotExist:
        raise ValidationError(
            {'detail': 'There is no category with the given slug.'}
        )

def publish_skill(*, slug:str) -> None:
    try:
        skill = Skill.objects.get(slug=slug)
        skill.status = True
        skill.save()
    except Skill.DoesNotExist:
        raise ValidationError(
            {'detail': 'There is no skill with the given slug.'}
        )
