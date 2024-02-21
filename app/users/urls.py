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

    path('profile/me/', apis.ProfileMeApiView.as_view(), name='profile-me'),
    path('profile/<str:uuid>/', apis.ProfileDetailApiView.as_view(), name='profile-detail'),
    path('profile/<str:uuid>/subscription/', apis.SubscriptionApiView.as_view(), name='subscription'),

    # ============ JWT URL's ============
    path('jwt/login/', TokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view())
]
