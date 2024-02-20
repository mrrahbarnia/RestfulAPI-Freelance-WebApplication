from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from users.models import (
    BaseUser,
    Profile
)
from ...services.users import register

REGISTRATION_URL = reverse('users:registration')
GET_PROFILE_URL = reverse('users:profile-me')


class TestPublicUserEndpoints(TestCase):
    """Test endpoints without authentication."""

    def setUp(self) -> None:
        self.client = APIClient()

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], payload['phone_number'])
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

        url = reverse('users:profile-detail', args=[anonymous_user.profile.uuid])
        response = self.client.get(url)
        anonymous_user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(anonymous_user.profile.views, 1)


class TestPrivateUserEndpoints(TestCase):
    """Test endpoints wit authentication."""

    def setUp(self) -> None:
        self.client = APIClient()
        phone_number = '09131111111'
        password = '1234@example.com'
        self.user_obj = register(
            phone_number=phone_number, email=None, password=password
        )
        self.client.force_authenticate(self.user_obj)
        
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
