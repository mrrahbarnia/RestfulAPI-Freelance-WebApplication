from django.db.models import QuerySet

from skill.models import (
    Category,
    Skill
)

def get_published_categories(*, name:str|None) -> QuerySet[Category]:
    if name:
        try:
            category = Category.objects.get(name=name)
            return category
        except Category.DoesNotExist:
            # TODO: Logging
            pass
    return Category.objects.filter(status=True)

def get_published_skills(*, category:Category|None) -> QuerySet[Skill]:
    if category:
        return Skill.objects.filter(category=category, status=True)
    else:
        return Skill.objects.filter(status=True)

def category_choices() -> QuerySet[Category]:
    # TODO: Caching
    return list(Category.objects.filter(status=True).values_list('name', flat=True))
