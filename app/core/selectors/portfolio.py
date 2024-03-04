from django.db.models import QuerySet

from users.models import BaseUser
from portfolio.models import Portfolio

def get_my_portfolios(*, user:BaseUser) -> QuerySet[Portfolio]:
    return Portfolio.objects.filter(
        profile__user=user
    ).only('title', 'description', 'cover_image')
