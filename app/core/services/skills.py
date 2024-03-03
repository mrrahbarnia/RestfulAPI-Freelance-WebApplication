from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db import transaction
from django.core.cache import cache
from rest_framework import serializers

from skill.models import (
    Skill,
    Category
)

def create_category(*, name:str) -> Category:
    return Category.objects.create(name=name, slug=slugify(name))

def create_skill(*, name:str, category:Category) -> Skill:
    return Skill.objects.create(name=name, category=category, slug=slugify(name))

@transaction.atomic
def publish_category(*, slug:str) -> None:
    category = Category.objects.filter(slug=slug).only('published')
    if category:
        category.update(published=True)
        cache.set(
            key='category_choices',
            value=list(Category.objects.filter(published=True).values_list('name', flat=True)),
            timeout=None
        )
    else:
        raise ValidationError(
            {'detail': 'There is no category with the given slug.'}
        )

def publish_skill(*, slug:str) -> None:
    skill = Skill.objects.filter(slug=slug).only('published')
    if skill:
        skill.update(published=True)
    else:
        raise ValidationError(
            {'detail': 'There is no skill with the given slug.'}
        )

def unpublish_category(*, slug:str) -> None:
    category = Category.objects.filter(slug=slug).only('published')
    if category:
        category.update(published=False)
    else:
        raise ValidationError(
            {'detail': 'There is no category with the given slug.'}
        )

def unpublish_skill(*, slug:str) -> None:
    skill = Skill.objects.filter(slug=slug).only('published')
    if skill:
        skill.update(published=False)
    else:
        raise ValidationError(
            {'detail': 'There is no skill with the given slug.'}
        )
