from django.db.models import QuerySet

from users.models import (
    BaseUser,
    Profile,
    Subscription
)

def get_profile(*, user:BaseUser) -> Profile:
    return Profile.objects.get(user=user)

def get_freelancers() -> QuerySet[Profile]:
    return Profile.objects.all().order_by('-score')

def my_followers(*, profile:Profile) -> QuerySet[Subscription]:
    return Subscription.objects.only('follower').filter(target=profile)

def my_followings(*, profile:Profile) -> QuerySet[Subscription]:
    return Subscription.objects.only('target').filter(follower=profile)
