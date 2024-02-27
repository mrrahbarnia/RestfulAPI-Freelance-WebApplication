from django.db.models import QuerySet

from skill.models import (
    Category,
    Skill
)

def get_categories(*, name:str|None) -> QuerySet[Category]:
    if name:
        try:
            category = Category.objects.get(name=name)
            return category
        except Category.DoesNotExist:
            # TODO: Logging
            pass
    return Category.objects.filter(status=True)

def get_skills(*, category:Category|None) -> QuerySet[Skill]:
    if category:
        return Skill.objects.filter(category=category, status=True)
    else:
        return Skill.objects.filter(status=True)
