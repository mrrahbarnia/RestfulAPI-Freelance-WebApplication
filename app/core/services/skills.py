from skill.models import (
    Skill,
    Category
)

def create_category(*, name:str) -> Category:
    return Category.objects.create(name=name)

def create_skill(*, name:str, category:Category) -> Skill:
    return Skill.objects.create(name=name, category=category)
