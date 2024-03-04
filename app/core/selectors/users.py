from django.core.cache import cache
from django.db.models import QuerySet

from skill.models import Skill
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
    cached_data = cache.get(f'followers_{profile}')
    if cached_data:
        return cached_data
    else:
        followers = Subscription.objects.only(
            'follower'
        ).select_related('follower').filter(target=profile)
        cache.set(key=f'followers_{profile}', value=followers, timeout=None)
        return followers

def my_followings(*, profile:Profile) -> QuerySet[Subscription]:
    cached_data = cache.get(f'followings_{profile}')
    if cached_data:
        return cached_data
    else:
        followings = Subscription.objects.only(
            'target'
        ).select_related('target').filter(follower=profile)
        cache.set(key=f'followings_{profile}', value=followings, timeout=None)
        return followings

def my_skills(*, user:BaseUser) -> QuerySet[Skill]:
    cached_skills = cache.get(f'{user}_skills')
    if cached_skills:
        return cached_skills
    else:
        skills = Skill.objects.filter(skill_profile__user=user).only('name', 'slug')
        cache.set(
            key=f'{user}_skills',
            value=skills,
            timeout=None
        )
        return skills
