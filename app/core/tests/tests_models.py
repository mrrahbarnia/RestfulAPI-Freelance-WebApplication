from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from users.models import BaseUser

User = get_user_model()


class TestModels(TestCase):

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
