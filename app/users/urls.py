from django.urls import path

from . import apis

app_name = 'users'

urlpatterns = [
    path('registration/', apis.RegistrationApiView.as_view(), name='registration')
]
