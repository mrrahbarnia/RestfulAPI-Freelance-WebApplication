"""
Layer for users services Business logics.
"""
import random

from django.db import transaction
from django.core.cache import cache
from rest_framework.exceptions import APIException
from rest_framework import serializers

from skill.models import Skill
from users.models import (
    BaseUser,
    Profile,
    Subscription,
    ProfileSkill
)

def otp_generator():
    """Generate OTP for verification."""
    otp = random.randint(100000, 999999)
    return otp


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

def send_otp(*, phone_number:str) -> None:
    otp = otp_generator()
    cache.set(key=f'otp_{otp}_{phone_number}', value=otp, timeout=60*2)
    # TODO: Sending OTP via sms...

def resend_otp(*, phone_number:str) -> None:
    try:
        BaseUser.objects.get(phone_number=phone_number)
        send_otp(phone_number=phone_number)
    except BaseUser.DoesNotExist:
        raise serializers.ValidationError(
            'There is no user with the provided phone number.',
        )

@transaction.atomic
def register(*, phone_number:str, email:str, password:str) -> BaseUser:
    user = create_user(phone_number=phone_number, password=password)
    send_otp(phone_number=phone_number)
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

def verify_otp(*, otp:int) -> None:
    cached_data = cache.keys(f'otp_{otp}_*') # 'otp_{otp}_{phone_number}'
    if cached_data: # Probably there is one cache data with this pattern so it doesn't take too long to process
        for otp_key in cached_data:
            phone_number = otp_key.split('_')[2]
            user = BaseUser.objects.get(phone_number=phone_number)
            user.is_active = True
            user.save()
            cache.delete(f'otp_{otp}_{phone_number}')
    else:
        raise APIException('The OTP has been expired or not valid.Get a new one...')

@transaction.atomic
def select_skill(*, user:BaseUser, slug:str) -> None:
    profile = Profile.objects.get(user=user)
    skill = Skill.objects.get(slug=slug)
    cache.delete(f'{user}_skills')
    if skill.published:
        profile.skills.add(skill)
        profile.save()
    else:
        raise serializers.ValidationError(
            'The provided skill is not published yet.'
        )

@transaction.atomic
def unselect_skill(*, user:BaseUser, slug:str) -> None:
    profile = Profile.objects.get(user=user)
    user_skills = ProfileSkill.objects.filter(profile_id=profile).filter(skill_id__slug=slug)
    cache.delete(f'{user}_skills')
    if user_skills:
        user_skills.delete()
    else:
        raise serializers.ValidationError(
            'There is no selected skill with the provided slug.'
        )