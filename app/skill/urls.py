from django.urls import path

from . import apis

app_name = 'skill'

urlpatterns = [
    path('categories/', apis.CategoryApiView.as_view(), name='categories'),
    path('skills/', apis.SkillApiView.as_view(), name='skills'),
]