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

    path('profile/me/', apis.ProfileMeApiView.as_view(), name='profile_me'),
    path('profile/<str:uuid>/', apis.ProfileDetailApiView.as_view(), name='profile_detail'),
    path('profile/<str:uuid>/subscription/', apis.SubscriptionApiView.as_view(), name='subscription'),
    path('freelancers/', apis.ListFreelancersApiView.as_view(), name='freelancers_list'),
    path('followers/', apis.ListMyFollowersApiView.as_view(), name='followers'),
    path('followings/', apis.ListMyFollowingsApiView.as_view(), name='followings'),
    path('otp/verification/', apis.OtpVerificationApiView.as_view(), name='verification'),
    path('otp/resend/', apis.ResendOtpApiView.as_view(), name='resend_otp'),
    path('profile/<str:slug>/select/', apis.SelectSkillApiView.as_view(), name='select_skill'),
    path('profile/skills/me/', apis.MySkillsApiView.as_view(), name='my_skills'),
    path('profile/<str:slug>/unselect/', apis.UnselectSkillApiView.as_view(), name='unselect_skill'),




    # ============ JWT URL's ============
    path('jwt/login/', TokenObtainPairView.as_view()),
    path('jwt/refresh/', TokenRefreshView.as_view()),
    path('jwt/verify/', TokenVerifyView.as_view())
]
