from django.urls import path

from . import apis

app_name = 'skill'

urlpatterns = [
    path('categories/published/', apis.CategoryApiView.as_view(), name='categories'),
    path('skills/published/', apis.SkillApiView.as_view(), name='skills'),
    path('category/<str:slug>/publish/', apis.CategoryDetailApiView.as_view(), name='category_detail'),
    path('skill/<str:slug>/publish/', apis.SkillDetailApiView.as_view(), name='skill_detail'),
]