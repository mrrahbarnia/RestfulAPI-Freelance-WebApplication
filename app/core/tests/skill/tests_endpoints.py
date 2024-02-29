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

CATEGORY_URL = reverse('skill:categories')
SKILL_URL = reverse('skill:skills')
PUB_CATEGORY_URL = reverse('skill:pub_categories')
PUB_SKILL_URL = reverse('skill:pub_skills')


class TestPublicSkillEndpoints(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_list_published_skills_with_unauthenticated_user_successfully(self):
        cat = create_category(name='Backend Developer')
        skill1 = create_skill(name='Django', category=cat)
        skill1.status = True
        skill1.save()
        skill2 = create_skill(name='FastAPI', category=cat)
        skill2.status = True
        skill2.save()
        create_skill(name='Go', category=cat)

        response = self.client.get(PUB_SKILL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_published_categories_with_unauthenticated_user_successfully(self):
        cat1 = create_category(name='Backend Development')
        cat1.status = True
        cat1.save()
        cat2 = create_category(name='UI')
        cat2.status = True
        cat2.save()

        response = self.client.get(PUB_CATEGORY_URL)

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
    
    def test_publish_category_by_unauthenticated_user_unsuccessfully(self):
        category = create_category(name='Backend')

        url = reverse('skill:category_detail', args=[category.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(category.status)


    def test_publish_skill_by_unauthenticated_user_unsuccessfully(self):
        category = create_category(name='Backend')
        skill = create_skill(category=category, name='Django')

        url = reverse('skill:skill_detail', args=[skill.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(skill.status)

    def test_get_all_categories_by_unauthenticated_user_unsuccessfully(self):
        response = self.client.get(CATEGORY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_skills_by_unauthenticated_user_unsuccessfully(self):
        response = self.client.get(SKILL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unpublish_category_unauthenticated_unsuccessfully(self):
        sample_category = create_category(name='Backend')
        sample_category.status = True
        sample_category.save()
        sample_category.refresh_from_db()
        url = reverse('skill:unpublish_category', args=[sample_category.slug])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unpublish_skill_unauthenticated_unsuccessfully(self):
        sample_category = create_category(name='Backend')
        sample_skill = create_skill(category=sample_category, name='Django')
        sample_skill.status = True
        sample_skill.save()
        sample_skill.refresh_from_db()
        url = reverse('skill:unpublish_skill', args=[sample_skill.slug])

        response = self.client.delete(url)

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

    def test_create_skill_without_existing_category_unsuccessfully(self):
        create_category(name='UI')
        payload = {
            "name": "React",
            "category": "Frontend"
        }

        response = self.admin_client.post(SKILL_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Skill.objects.filter(name=payload['name']).exists())

    def test_create_skill_with_existing_category_successfully(self):
        create_category(name='Backend')

        payload = {
            'name': 'FastAPI',
            'category': 'Backend'
        }

        response = self.admin_client.post(SKILL_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.all().count(), 1)
    
    def test_publish_category_by_normal_user_unsuccessfully(self):
        sample_category = create_category(name='Backend')

        url = reverse('skill:category_detail', args=[sample_category.slug])
        response = self.normal_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        sample_category.refresh_from_db()
        self.assertFalse(sample_category.status)

    def test_publish_skill_by_normal_user_unsuccessfully(self):
        sample_category = create_category(name='Backend')
        sample_skill = create_skill(name='Django', category=sample_category)

        url = reverse('skill:skill_detail', args=[sample_skill.slug])
        response = self.normal_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        sample_skill.refresh_from_db()
        self.assertFalse(sample_skill.status)

    def test_publish_category_by_admin_user_successfully(self):
        sample_category = create_category(name='Backend')
        self.assertFalse(sample_category.status)

        url = reverse('skill:category_detail', args=[sample_category.slug])
        response = self.admin_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sample_category.refresh_from_db()
        self.assertTrue(sample_category.status)

    def test_publish_skill_by_admin_user_successfully(self):
        sample_category = create_category(name='Backend')
        sample_skill = create_skill(name='Django', category=sample_category)

        url = reverse('skill:skill_detail', args=[sample_skill.slug])
        response = self.admin_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sample_skill.refresh_from_db()
        self.assertTrue(sample_skill.status)
    
    def test_get_all_categories_by_normal_user_unsuccessfully(self):
        response = self.normal_client.get(CATEGORY_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_skills_by_normal_user_unsuccessfully(self):
        response = self.normal_client.get(SKILL_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_categories_by_admin_user_successfully(self):
        create_category(name='Backend')
        create_category(name='Devops')

        response = self.admin_client.get(CATEGORY_URL)

        self.assertEqual(len(eval(response.content)), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_skills_by_admin_user_successfully(self):
        sample_category = create_category(name='Backend')
        create_skill(category=sample_category, name='Django')
        create_skill(category=sample_category, name='FastAPI')

        response = self.admin_client.get(SKILL_URL)

        self.assertEqual(len(eval(response.content)), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unpublish_category_with_normal_user_unsuccessfully(self):
        sample_category = create_category(name='Backend')
        sample_category.status = True
        sample_category.save()
        sample_category.refresh_from_db()
        url = reverse('skill:unpublish_category', args=[sample_category.slug])

        response = self.normal_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unpublish_skill_with_normal_user_unsuccessfully(self):
        sample_category = create_category(name='Backend')
        sample_skill = create_skill(category=sample_category, name='Django')
        sample_skill.status = True
        sample_skill.save()
        sample_skill.refresh_from_db()
        url = reverse('skill:unpublish_skill', args=[sample_skill.slug])

        response = self.normal_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unpublish_category_with_admin_user_successfully(self):
        sample_category = create_category(name='Backend')
        sample_category.status = True
        sample_category.save()
        sample_category.refresh_from_db()
        url = reverse('skill:unpublish_category', args=[sample_category.slug])

        response = self.admin_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unpublish_skill_with_admin_user_successfully(self):
        sample_category = create_category(name='Backend')
        sample_skill = create_skill(category=sample_category, name='Django')
        sample_skill.status = True
        sample_skill.save()
        sample_skill.refresh_from_db()
        url = reverse('skill:unpublish_skill', args=[sample_skill.slug])

        response = self.admin_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
