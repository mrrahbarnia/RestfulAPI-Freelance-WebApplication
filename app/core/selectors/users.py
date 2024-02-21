from django.db.models import QuerySet

from users.models import (
    BaseUser,
    Profile
)

def get_profile(*, user:BaseUser) -> Profile:
    return Profile.objects.get(user=user)

def get_freelancers() -> QuerySet[Profile]:
    return Profile.objects.all().order_by('-score')