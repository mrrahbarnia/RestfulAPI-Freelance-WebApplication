from django.contrib import admin

from .models import (
    BaseUser,
    Profile,
    Subscription
)

admin.site.register(BaseUser)
admin.site.register(Profile)
admin.site.register(Subscription)
