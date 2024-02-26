from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import BaseUser
from skill.models import (
    Category,
    Skill
)
from ...services.skills import (
    create_category,
    create_skill
)

CATEGORY_URL = reverse('skill:category')
SKILL_URL = reverse('skill:skill')


class TestPublicSkillEndpoints(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_list_skills_with_unauthenticated_user_successfully(self):
        cat = create_category(name='Backend Developer')
        create_skill(name='Django', category=cat)
        create_skill(name='FastAPI', category=cat)

        response = self.client.get(SKILL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_categories_with_unauthenticated_user_successfully(self):
        create_category(name='Backend Development')
        create_category(name='UI')

        response = self.client.get(CATEGORY_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_category_with_unauthenticated_user(self):
        payload = {'name': 'UI'}

        response = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_skill_with_unauthenticated_user(self):
        payload = {
            'name': 'Backend Development',
            'category': 'FastAPI'
        }

        response = self.client.post(SKILL_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateSkillEndpoints(TestCase):
    
    def setUp(self) -> None:
        self.normal_client = APIClient()
        self.admin_client = APIClient()
        self.admin = BaseUser.objects.create_superuser(
            phone_number='09131111111', password='1234@example.com'
        )
        self.user = BaseUser.objects.create_user(
            phone_number='09132222222', password='1234@example.com'
        )
        self.admin_client.force_authenticate(self.admin)
        self.normal_client.force_authenticate(self.user)
    
    def test_create_category_with_normal_user(self):
        payload = {'name': 'UI'}

        response = self.normal_client.post(CATEGORY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_skill_with_normal_user(self):
        payload = {
            'name': 'Backend Development',
            'category': 'FastAPI'
        }

        response = self.normal_client.post(SKILL_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_with_admin_user_successfully(self):
        payload = {'name': 'UI'}

        response = self.admin_client.post(CATEGORY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.all().count(), 1)

    def test_create_skill_with_admin_user_successfully(self):
        payload = {
            'name': 'Backend Development',
            'category': 'FastAPI'
        }

        response = self.admin_client.post(SKILL_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.all().count(), 1)
