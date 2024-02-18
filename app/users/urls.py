from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import apis

app_name = 'users'

urlpatterns = [
    path('registration/', apis.RegistrationApiView.as_view(), name='registration'),
    path('jwt/login/', TokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view())
]
