# import os
# import uuid

# from django.db import models

# from skill.models import Skill
# from core.timestamp import TimeStamp
# from users.models import Profile

# def portfolio_cover_img_path(instance, file_name):
#     """Generating unique path for portfolio cover images."""
#     ext = os.path.splitext(file_name)[1]
#     unique_name = f'{uuid.uuid4()}{ext}'

#     return os.path.join('uploads', 'portfolio', unique_name)


# class Portfolio(TimeStamp):
#     profile = models.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name='portfolio'
#     )
#     title = models.CharField(max_length=250)
#     slug = models.CharField(max_length=None, db_index=True)
#     description = models.CharField(max_length=1000, null=True, blank=True)
#     views = models.PositiveIntegerField(default=0)
#     cover_image = models.ImageField(upload_to=portfolio_cover_img_path, null=True, blank=True)
#     skills = models.ManyToManyField(
#         Skill, related_name='skill_portfolio', through='PortfolioSkill'
#     )
#     likes = models.PositiveIntegerField(default=0)

#     def __str__(self) -> str:
#         return f'{self.profile} >> {self.title}'


# class PortfolioImage(TimeStamp):
#     portfolio = models.ForeignKey(
#         Portfolio, on_delete=models.CASCADE, related_name='portfolio_image'
#     )

#     def __str__(self) -> str:
#         return self.portfolio


# class PortfolioComment(TimeStamp):
#     portfolio = models.ForeignKey(
#         Portfolio, on_delete=models.CASCADE, related_name='portfolio_comment'
#     )

#     def __str__(self) -> str:
#         return self.portfolio


# class PortfolioSkill(models.Model):
#     portfolio_id = models.ForeignKey(
#         Portfolio, on_delete=models.CASCADE, related_name='portfolio_skill_prt'
#     )
#     skill_id = models.ForeignKey(
#         Skill, on_delete=models.CASCADE, related_name='portfolio_skill_sk'
#     )

#     class Meta:
#         unique_together = ('portfolio_id', 'skill_id')

#     def __str__(self) -> str:
#         return f'{self.portfolio_id.title} >> {self.skill_id}'

#     def clean(self) -> None:

#         from django.core.exceptions import ValidationError

#         qs = list(Skill.objects.filter(
#             skill_profile=self.portfolio_id.profile
#         ).values_list('name', flat=True))
#         if str(self.skill_id) not in qs:
#             raise ValidationError(
#                 'This profile has not the provided skills for this portfolio.'
#             )
