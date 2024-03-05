from django.utils.text import slugify
from django.db.models import F
from rest_framework import serializers

from portfolio.models import Portfolio
from users.models import BaseUser

def create_portfolio(
        *, user:BaseUser, title:str|None,
        description:str|None, cover_image:str|None
) -> Portfolio:
    portfolio = Portfolio(
        profile=user.profile,
        title=title,
        slug=slugify(title),
        description=description or None,
        cover_image=cover_image or None
    )
    portfolio.full_clean()
    portfolio.save()
    return portfolio

def get_portfolio(*, slug:str) -> Portfolio:
    portfolio = Portfolio.objects.get(slug=slug)
    portfolio.views = F('views') + 1
    portfolio.save()
    return portfolio

def get_portfolio_for_delete(*, slug:str) -> None:
    try:
        portfolio = Portfolio.objects.get(slug=slug)
        return portfolio
    except Portfolio.DoesNotExist:
        raise serializers.ValidationError(
            'There is no portfolio with the provided slug.'
        )
