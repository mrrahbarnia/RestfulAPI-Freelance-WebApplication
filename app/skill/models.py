from django.db import models

from core.timestamp import TimeStamp


class Skill(TimeStamp):
    # TODO: Only admins has permissions to create skills
    name = models.CharField(max_length=250)
    category = models.ForeignKey(
        'Category', models.ForeignKey, related_name='skill_category'
    )

    def __str__(self) -> str:
        return self.name


class Category(TimeStamp):
    # TODO: Only admins has permissions to create categories
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name
