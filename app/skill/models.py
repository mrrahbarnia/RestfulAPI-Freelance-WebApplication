from django.db import models

from core.timestamp import TimeStamp


class Skill(TimeStamp):
    name = models.CharField(max_length=250, unique=True)
    slug = models.CharField(max_length=250, db_index=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='skill_category'
    )
    published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Category(TimeStamp):
    name = models.CharField(max_length=250, unique=True)
    slug = models.CharField(max_length=250, db_index=True)
    published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
