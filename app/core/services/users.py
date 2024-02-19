"""
Layer for users services Business logics.
"""
from users.models import (
    BaseUser,
    Profile
)

def create_user(*, phone_number:str, password:str) -> BaseUser:
    user = BaseUser.objects.create_user(
        phone_number=phone_number,
        password=password
    )
    return user

def create_profile(*, user:BaseUser, email:str|None) -> Profile:
    return Profile.objects.create(user=user, email=email)

def register(*, phone_number:str, email:str, password:str) -> BaseUser:
    user = create_user(phone_number=phone_number, password=password)
    create_profile(user=user, email=email)
    return user
