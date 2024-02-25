from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from users.models import (
    BaseUser,
    Profile
)
from skill.models import (
    Skill,
    Category
)
from portfolio.models import (
    Portfolio,
    PortfolioSkill
)

User = get_user_model()


class TestUserModels(TestCase):

    def test_create_user_successfully(self):
        User.objects.create_user(
            phone_number='09131111111',
            password='1234@example.com'
        )

        self.assertTrue(
            BaseUser.objects.filter(phone_number='09131111111').exists()
        )
    
    def test_create_user_unsuccessfully(self):
        """Create user with more than 11 digits phone number."""
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                phone_number='0913111111',
                password='1234@example.com'
            )
        
    def test_create_profile_successfully(self):
        user_obj = User.objects.create_user(
            phone_number='09131111111',
            password='1234@example.com'
        )
        profile_obj = Profile.objects.create(
            user=user_obj,
            email='user@example.com',
            bio='Sample bio'
        )

        self.assertTrue(Profile.objects.filter(
            email=profile_obj.email
        ).exists())
    
    def test_create_portfolio_with_not_provided_skills(self):
        """
        Test creating portfolio with some skills which
        not existing in profile skills unsuccessfully.
        """
        sample_user = BaseUser.objects.create_user(
            phone_number='09131111111', password='1234@example.com'
        )
        sample_profile = Profile.objects.create(
            user=sample_user, email='admin@example.com'
        )
        sample_category = Category.objects.create(name='Backend development')
        sample_skill1 = Skill.objects.create(
            name='Django', category=sample_category
        )
        sample_skill2 = Skill.objects.create(
            name='FastAPI', category=sample_category
        )
        sample_portfolio = Portfolio.objects.create(
            profile=sample_profile,
            title='Sample portfolio',
            slug='sample-portfolio'
        )
        sample_profile.skills.add(sample_skill1)

        portfolio_skill = PortfolioSkill(
            portfolio_id=sample_portfolio, skill_id=sample_skill2
        )
        with self.assertRaises(ValidationError):
            portfolio_skill.full_clean()
