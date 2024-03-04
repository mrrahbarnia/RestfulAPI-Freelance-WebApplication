from django.utils.text import slugify
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

    