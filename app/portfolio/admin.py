from django.contrib import admin

from .models import (
    Portfolio,
    PortfolioSkill,
    PortfolioImage,
    PortfolioComment
)

admin.site.register(Portfolio)
admin.site.register(PortfolioSkill)
admin.site.register(PortfolioImage)
admin.site.register(PortfolioComment)
