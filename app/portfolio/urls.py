from django.urls import path

from . import apis

app_name = 'portfolio'

urlpatterns = [
    path('create/', apis.CreatePortfolioApiView.as_view(), name='create_portfolio'),
    path('me/', apis.MyPortfoliosApiView.as_view(), name='my_portfolios'),
    path('<str:slug>/', apis.PortfolioDetailApiView.as_view(), name='portfolio_detail'),
    path('comment/all/', apis.CommentApiView.as_view(), name='comment'),
    path('comment/<str:pk>/delete/', apis.DeleteCommentApiView.as_view(), name='delete_comment'),
    path('<str:slug>/publish/', apis.PublishPortfolioApiView.as_view(), name='publish_portfolio')
]
