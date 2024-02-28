from django.urls import path

from . import apis

app_name = 'skill'

urlpatterns = [
    path('categories/all/', apis.CategoryApiView.as_view(), name='categories'),
    path('skills/all/', apis.SkillApiView.as_view(), name='skills'),
    path('categories/published/', apis.PubCategoryApiView.as_view(), name='pub_categories'),
    path('skills/published/', apis.PubSkillApiView.as_view(), name='pub_skills'),
    path('category/<str:slug>/publish/', apis.CategoryDetailApiView.as_view(), name='category_detail'),
    path('skill/<str:slug>/publish/', apis.SkillDetailApiView.as_view(), name='skill_detail'),
]