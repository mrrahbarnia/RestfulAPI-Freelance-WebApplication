from django.test import TestCase
from django.core.exceptions import ValidationError

from users.models import (
    BaseUser,
    Profile
)
from ...services.users import register


class TestUserServices(TestCase):

    def test_register_successfully(self):
        phone_number = '09131111111'
        password = '1234@example.com'

        register(
            phone_number=phone_number, email=None, password=password
        )

        self.assertTrue(BaseUser.objects.filter(
            phone_number=phone_number
        ).exists())
        self.assertEqual(Profile.objects.all().count(), 1)

    def test_register_unsuccessfully(self):
        phone_number = '0913111111'
        password = '1234@example.com'

        with self.assertRaises(ValidationError):
            register(
                phone_number=phone_number, email=None, password=password
            )
