from django.db import models

from core.timestamp import TimeStamp


class Skill(TimeStamp):
    name = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(
        'Category', models.ForeignKey, related_name='skill_category'
    )
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Category(TimeStamp):
    name = models.CharField(max_length=250, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
