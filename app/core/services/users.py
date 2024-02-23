"""
Layer for users services Business logics.
"""
from django.db import transaction
from django.core.cache import cache
from rest_framework.exceptions import APIException

from users.models import (
    BaseUser,
    Profile,
    Subscription
)

def create_user(*, phone_number:str, password:str) -> BaseUser:
    user = BaseUser.objects.create_user(
        phone_number=phone_number,
        password=password
    )
    user.full_clean()
    return user

@transaction.atomic
def create_profile(*, user:BaseUser, email:str|None) -> Profile:
    profile = Profile.objects.create(user=user, email=email)
    cache.set(key=f'{profile}', value=profile, timeout=None)
    return profile

def update_profile(
        *, user:BaseUser, email:str|None, bio:str|None,
        image:str|None, age:int|None, sex:str|None, city:str|None
) -> Profile:
    profile_obj = Profile.objects.get(user=user)

    profile_obj.email = email or profile_obj.email
    profile_obj.bio = bio or profile_obj.bio
    profile_obj.image = image or profile_obj.image
    profile_obj.age = age or profile_obj.age
    profile_obj.sex = sex or profile_obj.sex
    profile_obj.city = city or profile_obj.city

    profile_obj.save()
    return profile_obj

@transaction.atomic
def register(*, phone_number:str, email:str, password:str) -> BaseUser:
    user = create_user(phone_number=phone_number, password=password)
    create_profile(user=user, email=email)
    return user

def profile_detail(*, uuid:str) ->Profile:
    profile_object = cache.get(uuid)
    if profile_object:
        profile_object.views += 1
        cache.set(key=profile_object, value=profile_object, timeout=None)
        return profile_object
    else:
        profile = Profile.objects.get(uuid=uuid)
        return profile
    # TODO:Create a scheduling for inserting profile data into database with celery and rabbitmq

@transaction.atomic
def subscribe(*, follower:Profile, target_uuid:str) -> Subscription:
    """
    Create subscription method by passing two arguments:
    1 - follower    >> User instance of the follower
    2 - target_uuid >> The uuid that belongs to target_user
    """
    try:
        target_user = Profile.objects.get(uuid=target_uuid)
    except Profile.DoesNotExist:
        raise APIException(
            'There is no user with provided uuid.'
        )
    subscription = Subscription(follower=follower, target=target_user)
    subscription.full_clean()
    subscription.save()

    cache.delete(f'followings_{follower}')
    cache.delete(f'followers_{target_user}')

    return subscription

def unsubscribe(*, un_follower:Profile, target_uuid:str) -> Subscription:
    """
    Deleting subscription method by passing two arguments:
    1 - un_follower   >> User instance of the follower
    2 - target_uuid   >> The uuid that belongs to target_user
    """
    try:
        target_user = Profile.objects.get(uuid=target_uuid)
    except Profile.DoesNotExist:
        raise APIException(
            'There is no user with provided uuid.'
        )
    try:
        subscription = Subscription.objects.get(
            follower=un_follower, target=target_user
        )
    except Subscription.DoesNotExist:
        raise APIException(
            'The target user has not already been followed.'
        )
    subscription.delete()
    # TODO:Caching
