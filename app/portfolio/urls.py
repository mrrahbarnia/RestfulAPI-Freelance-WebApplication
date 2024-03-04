from django.urls import path

from . import apis

app_name = 'portfolio'

urlpatterns = [
    path('create/', apis.CreatePortfolioApiView.as_view(), name='create_portfolio'),
]
