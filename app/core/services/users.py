"""
Layer for users services Business logics.
"""
from django.db import transaction
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

def create_profile(*, user:BaseUser, email:str|None) -> Profile:
    return Profile.objects.create(user=user, email=email)

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

def register(*, phone_number:str, email:str, password:str) -> BaseUser:
    user = create_user(phone_number=phone_number, password=password)
    create_profile(user=user, email=email)
    return user

def profile_detail(*, uuid:str) ->Profile:
    profile = Profile.objects.get(uuid=uuid)
    profile.views += 1
    profile.save()
    # TODO: Caching views for profile views
    return profile

def subscribe(*, follower:BaseUser, target_uuid:str) -> Subscription:
    """
    Create subscription method by passing two arguments:
    1 - follower >> User instance of the follower
    2 - target_uuid     >> The uuid that belongs to target_user
    """
    try:
        target_user = BaseUser.objects.get(profile__uuid=target_uuid)
    except BaseUser.DoesNotExist:
        raise APIException(
            'There is no user with provided uuid.'
        )
    subscription = Subscription.objects.create(follower=follower, target=target_user)
    # TODO:Caching
    return subscription

@transaction.atomic
def unsubscribe(*, un_follower:BaseUser, target_uuid:str) -> Subscription:
    """
    Deleting subscription method by passing two arguments:
    1 - un_follower >> User instance of the follower
    2 - target_uuid        >> The uuid that belongs to target_user
    """
    try:
        target_user = BaseUser.objects.get(profile__uuid=target_uuid)
    except BaseUser.DoesNotExist:
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
