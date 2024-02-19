"""
Layer for users services Business logics.
"""
from PIL import Image as img
from users.models import (
    BaseUser,
    Profile
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

    profile_obj.email = email
    profile_obj.bio = bio
    profile_obj.image = image
    profile_obj.age = age
    profile_obj.sex = sex
    profile_obj.city = city

    profile_obj.save()
    return profile_obj

def register(*, phone_number:str, email:str, password:str) -> BaseUser:
    user = create_user(phone_number=phone_number, password=password)
    create_profile(user=user, email=email)
    return user
