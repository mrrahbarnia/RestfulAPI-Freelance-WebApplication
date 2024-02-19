import os
import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import (
    BaseUserManager as BUM,
    AbstractBaseUser
)

from app.timestamp import TimeStamp
from .validators import (
    profile_image_size_validator,
    age_validator
)

def generate_uuid():
    """Generating uuid for using in profile_detail url."""
    return str(uuid.uuid4()).split('-')[0]

def profile_img_path(instance, file_name):
    """Generating unique path for profile images."""
    ext = os.path.splitext(file_name)[1]
    unique_name = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'profile', unique_name)


class BaseUserManager(BUM):
    
    def create_user(
            self, phone_number, password=None,
            is_active=False, is_admin=False
    ):
        if not phone_number:
            raise ValueError('Users must have a phone number.')
        
        user = self.model(
            phone_number=phone_number,
            is_active=is_active, is_admin=is_admin
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number=phone_number,
            is_active=True,
            is_admin=True,
            password=password
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user



class BaseUser(TimeStamp, AbstractBaseUser, PermissionsMixin):

    phone_number = models.CharField(
        verbose_name='phone number', max_length=12, unique=True
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"

    objects = BaseUserManager()

    def clean(self) -> None:
        """Only when calling full_clean method in
        business logics this module is gonna import"""
        from django.core.exceptions import ValidationError

        if len(self.phone_number) != 11:
            raise ValidationError(
                'The length of phone number must be exact 11 digits.'
            )

    def __str__(self) -> str:
        return self.phone_number

    def is_staff(self):
        return self.is_admin

PLAN_CHOICES = [
    ('FREE', 'Free'),
    ('BRONZE', 'Bronze'),
    ('SILVER', 'Silver'),
    ('GOLD', 'Gold')
]

SEX = [
    ('M', 'Male'),
    ('F', 'Female')
]


class Profile(models.Model):
    user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, related_name='profile'
    )
    email = models.EmailField(
        verbose_name='email address',
        null=True, blank=True
    )
    bio = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(
        validators=[profile_image_size_validator],
        upload_to=profile_img_path, null=True, blank=True
    )
    age = models.PositiveIntegerField(
        validators=[age_validator], null=True, blank=True
    )
    plan_type = models.CharField(
        max_length=6, choices=PLAN_CHOICES, default='FREE'
    )
    balance = models.DecimalField(
        max_digits=20, decimal_places=3, default=0
    )
    score = models.PositiveIntegerField(default=0)
    sex = models.CharField(max_length=2, choices=SEX, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    uuid = models.CharField(max_length=None, default=generate_uuid)

    def __str__(self) -> str:
        return self.user.phone_number


# TODO:class Portfolio(models.Model)
# TODO:class Comment(models.Model)
# TODO:class Follow(models.Model)
# TODO:class Skill(models.Model)
