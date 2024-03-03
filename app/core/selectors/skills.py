from django.db.models import QuerySet
from django.core.cache import cache
from rest_framework import serializers

from skill.models import (
    Category,
    Skill
)

def get_published_categories(*, name:str|None) -> QuerySet[Category]:
    if name:
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            # TODO: Logging
            raise serializers.ValidationError(
                'There is no existing category with the provided name.'
            )
    return Category.objects.filter(published=True).only('name', 'slug')

def get_published_skills(*, category:Category|None) -> QuerySet[Skill]:
    if category:
        return Skill.objects.filter(category=category, published=True).only('name', 'slug')
    else:
        return Skill.objects.filter(published=True).only('name', 'slug')

def category_choices() -> QuerySet[Category]:
    cached_data = cache.get('category_choices')
    if cached_data:
        return cached_data
    else:
        return list(Category.objects.filter(published=True).values_list('name', flat=True))

def get_all_categories() -> QuerySet[Category]:
    return Category.objects.all().only('name', 'published', 'slug')

def get_all_skills() -> QuerySet[Skill]:
    return Skill.objects.all().only('name', 'published', 'slug')
