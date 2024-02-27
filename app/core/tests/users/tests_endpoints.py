from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status

from users.models import (
    BaseUser,
    Profile
)
from ...services.users import (
    register,
    subscribe
)

REGISTRATION_URL = reverse('users:registration')
GET_PROFILE_URL = reverse('users:profile_me')
GET_FREELANCERS_URL = reverse('users:freelancers_list')
FOLLOWERS_URL = reverse('users:followers')
FOLLOWINGS_URL = reverse('users:followings')
VERIFICATION_URL = reverse('users:verification')
RESEND_OTP_URL = reverse('users:resend_otp')


class TestPublicUserEndpoints(TestCase):
    """Test endpoints wit unauthenticated client."""

    def setUp(self) -> None:
        self.client = APIClient()
    
    def tearDown(self) -> None:
        cache.delete_pattern('*')

    def test_registration_endpoint_successfully(self):
        payload = {
            'phone_number': '09131111111',
            'email': 'example@gmail.com',
            'password': '1234@example.com',
            'confirm_password': '1234@example.com',
        }

        response = self.client.post(REGISTRATION_URL, payload, format='json')
        user_obj = BaseUser.objects.get(phone_number=payload['phone_number'])

        self.assertTrue(Profile.objects.filter(user=user_obj).exists(), True)
        self.assertEqual(Profile.objects.all().count(), 1)
        self.assertEqual(user_obj.is_active, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], payload['phone_number'])
        self.assertIn('OTP', response.data)
        self.assertTrue(
            BaseUser.objects.filter(
                phone_number=payload['phone_number']
            ).exists()
        )

    def test_registration_endpoint_unsuccessfully(self):
        payload = {
            'phone_number': '0913111111',
            'password': '123',
            'confirm_password': '123',
        }

        response = self.client.post(REGISTRATION_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            BaseUser.objects.filter(
                phone_number=payload['phone_number']
            ).exists()
        )
    
    def test_retrieve_profile_successfully(self):
        response = self.client.get(GET_PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_detail_profile_with_increasing_views(self):
        anonymous_user = register(
            phone_number='09131111111', email=None, password='1234@example.com'
        )

        url = reverse('users:profile_detail', args=[anonymous_user.profile.uuid])
        response = self.client.get(url)
        anonymous_user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['views'], 1)

    def test_get_freelancers_list_url(self):
        response = self.client.get(GET_FREELANCERS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_my_followers_with_unauthenticated_user(self):
        response = self.client.get(FOLLOWERS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_my_followers_with_unauthenticated_user(self):
        response = self.client.get(FOLLOWINGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_resend_otp_endpoint_with_existing_phone_number(self):
        register(
            phone_number='09131111111', email=None, password='1234@example.com'
        )
        payload = {
            'phone_number': '09131111111'
        }
        response = self.client.post(RESEND_OTP_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'OTP was resent successfully.')

    def test_resend_otp_endpoint_with_not_existing_phone_number(self):
        payload = {
            'phone_number': '09131111111'
        }
        response = self.client.post(RESEND_OTP_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual((eval(response.content)), ['There is no user with the provided phone number.'])

    @patch('core.services.users.otp_generator')
    def test_set_cached_otp_after_registration(self, mocked):
        otp = 123456
        mocked.return_value = otp
        phone_number='09131111111'
        register(
            phone_number=phone_number, email=None, password='1234@example.com'
        )

        self.assertTrue(cache.get(f'otp_{otp}_{phone_number}'))


class TestPrivateUserEndpoints(TestCase):
    """Test endpoints with authenticated client."""

    def setUp(self) -> None:
        self.client = APIClient()
        phone_number = '09131111111'
        password = '1234@example.com'
        self.user_obj = register(
            phone_number=phone_number, email=None, password=password
        )
        self.client.force_authenticate(self.user_obj)
    
    def tearDown(self) -> None:
        cache.delete_pattern('*')
        
    def test_retrieve_profile_successfully(self):
        response = self.client.get(GET_PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_partially_update_profile_successfully(self):
        payload = {
            'email': 'edited@gmail.com',
        }
        response = self.client.patch(GET_PROFILE_URL, payload)
        self.user_obj.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user_obj.profile.email, payload['email'])
    
    def test_subscribe_endpoint_successfully(self):
        sample_user = register(
            phone_number='09131234567',
            email='sample_user@gmail.com',
            password='1234@example.com'
        )
        url = reverse('users:subscription', args=[sample_user.profile.uuid])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sample_user.profile.target.all().count(), 1)
        self.assertEqual(self.user_obj.profile.follower.all().count(), 1)
    
    def test_unsubscribe_endpoint_successfully(self):
        sample_user = register(
            phone_number='09131234567', email=None, password='1234@example.com'
        )
        subscribe(follower=self.user_obj.profile, target_uuid=sample_user.profile.uuid)

        url = reverse('users:subscription', args=[sample_user.profile.uuid])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user_obj.profile.target.all().count(), 0)
    
    def test_list_my_followers_with_authenticated_user(self):
        user1 = register(
            phone_number='09132222222',
            email='sample_user@gmail.com',
            password='1234@example.com'
        )
        user2 = register(
            phone_number='09133333333',
            email='sample_user@gmail.com',
            password='1234@example.com'
        )
        subscribe(follower=user1.profile, target_uuid=self.user_obj.profile.uuid)
        subscribe(follower=user1.profile, target_uuid=user2.profile.uuid)
        response = self.client.get(FOLLOWERS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_my_followings_with_authenticated_user(self):
        user1 = register(
            phone_number='09132222222',
            email='sample_user@gmail.com',
            password='1234@example.com'
        )
        user2 = register(
            phone_number='09133333333',
            email='sample_user@gmail.com',
            password='1234@example.com'
        )
        subscribe(follower=self.user_obj.profile, target_uuid=user1.profile.uuid)
        subscribe(follower=user1.profile, target_uuid=user2.profile.uuid)
        response = self.client.get(FOLLOWINGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)