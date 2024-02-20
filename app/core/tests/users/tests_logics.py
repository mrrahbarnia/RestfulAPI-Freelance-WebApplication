from django.test import TestCase
from django.core.exceptions import ValidationError

from users.models import (
    BaseUser,
    Profile
)
from ...selectors.users import (
    get_profile,
    profile_detail
)
from ...services.users import (
    register,
    update_profile
)


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

    def test_get_profile(self):
        phone_number = '09131111111'
        password = '1234@example.com'

        user = register(
            phone_number=phone_number, email=None, password=password
        )

        profile_obj = get_profile(user=user)
        self.assertEqual(profile_obj.user.phone_number, phone_number)

    def test_update_profile(self):
        phone_number = '09131111111'
        password = '1234@example.com'
        email = 'example@gmail.com'

        user = register(
            phone_number=phone_number, email=email, password=password
        )

        edited_email = 'edited@gmail.com'
        edited_bio = 'Edited bio'

        update_profile(
            user=user,
            email=edited_email,
            bio=edited_bio,
            image=None,
            age=None,
            sex=None,
            city=None
        )

        user.refresh_from_db()

        self.assertNotEqual(user.profile.email, email)
        self.assertEqual(user.profile.email, edited_email)

    def test_profile_detail(self):
        phone_number = '09131111111'
        password = '1234@example.com'
        email = 'example@gmail.com'
        user = register(
            phone_number=phone_number, email=email, password=password
        )
        profile_detail(uuid=user.profile.uuid)

        self.assertTrue(Profile.objects.filter(
            uuid=user.profile.uud
        ).exists())
        self.assertEqual(Profile.objects.all().count())
