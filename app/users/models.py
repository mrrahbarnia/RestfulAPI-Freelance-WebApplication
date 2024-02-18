from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import (
    BaseUserManager as BUM,
    AbstractBaseUser
)

from app.timestamp import TimeStamp


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
                'The phone number must exactly be 11 digits.'
            )

    def __str__(self) -> str:
        return self.phone_number

    def is_staff(self):
        return self.is_admin
