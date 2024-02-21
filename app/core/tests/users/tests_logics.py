from django.test import TestCase
from django.core.exceptions import ValidationError

from users.models import (
    BaseUser,
    Profile
)
from ...selectors.users import (
    get_profile,
    get_freelancers,
)
from ...services.users import (
    register,
    update_profile,
    profile_detail,
    subscribe,
    unsubscribe
)


class TestUserServices(TestCase):

    def setUp(self) -> None:
        self.phone_number = '09131111111'
        self.password = '1234@example.com'
        self.email = 'example@gmail.com'
        self.sample_user = register(
            phone_number=self.phone_number, email=self.email, password=self.password
        )

    def test_register_successfully(self):

        self.assertTrue(BaseUser.objects.filter(
            phone_number=self.phone_number
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

        profile_obj = get_profile(user=self.sample_user)
        self.assertEqual(profile_obj.user.phone_number, self.phone_number)

    def test_update_profile(self):

        edited_email = 'edited@gmail.com'
        edited_bio = 'Edited bio'

        update_profile(
            user=self.sample_user,
            email=edited_email,
            bio=edited_bio,
            image=None,
            age=None,
            sex=None,
            city=None
        )

        self.sample_user.refresh_from_db()

        self.assertNotEqual(self.sample_user.profile.email, self.email)
        self.assertEqual(self.sample_user.profile.email, edited_email)

    def test_profile_detail(self):
        profile_detail(uuid=self.sample_user.profile.uuid)

        self.assertTrue(Profile.objects.filter(
            uuid=self.sample_user.profile.uuid
        ).exists())
        self.assertEqual(Profile.objects.all().count(), 1)

    def test_subscribe_logic(self):
        user1 = register(
            phone_number='09132222222', email=None, password='1234@example.com'
        )
        subscribe(follower=self.sample_user, target_uuid=user1.profile.uuid)

        self.assertEqual(user1.target.all().count(), 1)

    def test_unsubscribe_logic(self):
        user1 = register(
            phone_number='09132222222', email=None, password='1234@example.com'
        )
        subscribe(follower=self.sample_user, target_uuid=user1.profile.uuid)
        self.assertEqual(user1.target.all().count(), 1)

        unsubscribe(un_follower=self.sample_user, target_uuid=user1.profile.uuid)
        self.assertEqual(user1.target.all().count(), 0)

    def test_list_freelancers(self):
        user1 = register(
            phone_number='09132222222', email=None, password='1234@example.com'
        )
        user2 = register(
            phone_number='09133333333', email=None, password='1234@example.com'
        )
        self.sample_user.profile.score = 100
        user1.profile.score = 90
        user2.profile.score = 120
        self.sample_user.save()
        user1.save()
        user2.save()

        freelancers = get_freelancers()
        self.assertEqual(len(freelancers), 3)
        self.assertEqual(freelancers[0], user2.profile)
        self.assertEqual(freelancers[1], self.sample_user.profile)
        self.assertEqual(freelancers[2], user1.profile)
