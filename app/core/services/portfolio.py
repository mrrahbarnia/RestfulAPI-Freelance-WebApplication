from django.utils.text import slugify
from django.db.models import F
from rest_framework import serializers

from portfolio.models import (
    Portfolio,
    PortfolioComment
)
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

def publish_portfolio(*, slug:str) -> None:
    try:
        portfolio = Portfolio.objects.get(slug=slug)
        portfolio.published = True
        portfolio.save()
        return portfolio
    except Portfolio.DoesNotExist:
        raise serializers.ValidationError(
            'There is no portfolio with the provided slug.'
        )

def create_comment(
        *, user:BaseUser, slug:str, comment:str
) -> PortfolioComment:
    try:
        portfolio = Portfolio.objects.get(slug=slug)
    except Portfolio.DoesNotExist:
        raise serializers.ValidationError(
            'There is no portfolio with the provided slug.'
        )
    return PortfolioComment.objects.create(
        user=user, portfolio=portfolio, comment=comment
    )

def get_portfolio_comment_for_delete(*, pk:int) -> None:
    try:
        comment = PortfolioComment.objects.get(pk=pk)
        return comment
    except PortfolioComment.DoesNotExist:
        raise serializers.ValidationError(
            'There is no comment with the provided primary key.'
        )