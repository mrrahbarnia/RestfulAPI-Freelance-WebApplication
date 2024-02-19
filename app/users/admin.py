from django.contrib import admin

from .models import (
    BaseUser,
    Profile
)

admin.site.register(BaseUser)
admin.site.register(Profile)