from django.contrib import admin

from .models import (
    BaseUser,
    Profile,
    Subscription,
    ProfileSkill
)

admin.site.register(BaseUser)
admin.site.register(Profile)
admin.site.register(Subscription)
admin.site.register(ProfileSkill)
