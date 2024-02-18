"""
Layer for users services Business logics.
"""
from users.models import BaseUser

def register(*, phone_number:str, password:str) -> BaseUser:
    user = BaseUser.objects.create_user(
        phone_number=phone_number,
        password=password
    )
    return user
