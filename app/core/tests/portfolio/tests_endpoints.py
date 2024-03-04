from django.test import TestCase
from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from users.models import BaseUser
from core.selectors.portfolio import (
    get_my_portfolios
)
from core.services.skills import (
    create_category,
    create_skill,
    publish_category,
    publish_skill
)
from core.services.users import (
    register,
    create_profile,
    select_skill
)

PORTFOLIO_URL = reverse('portfolio:portfolio')
LIST_MY_PORTFOLIOS_URL = reverse('portfolio:my_portfolios')


class TestPublicEndpoints(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
    
    # def tearDown(self) -> None:
    #     cache.delete_pattern('*')

    def test_create_portfolio_unauthenticated_unsuccessfully(self):
        response = self.client.post(PORTFOLIO_URL, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_list_portfolios_unauthenticated_unsuccessfully(self):
    #     response = self.client.get(LIST_MY_PORTFOLIOS_URL)

    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPublicEndpoints(TestCase):

    def setUp(self) -> None:
        """
        Creating two client in this section:
        1 - normal client without permission to do some admins stuff.
        2 - admin client for doing everything.
        """
        self.normal_user = register(
            phone_number='09131111111',
            email='normal@example.com',
            password='1234@example.com'
        )
        self.normal_user.is_active = True
        self.normal_user.save()
        self.normal_client = APIClient()
        self.normal_client.force_authenticate(self.normal_user)

        self.admin_user = BaseUser.objects.create_superuser(
            phone_number='09132222222', password='1234@example.com'
        )
        create_profile(user=self.admin_user, email='admin@example.com')
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(self.admin_user)

    # def tearDown(self) -> None:
    #     cache.delete_pattern('*')
    
    def test_create_portfolio_authenticated_successfully(self):
        payload = {
            'title': 'New portfolio',
            'description': 'This is a very professional portfolio.',
        }
        response = self.client.post(PORTFOLIO_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_list_portfolios_authenticated_successfully(self):
    #     sample_category = create_category(name='Backend Development')
    #     sample_skill1 = create_skill(category=sample_category, name='Django')
    #     # sample_skill2 = create_skill(category=sample_category, name='FastAPI')

    #     select_skill(user=self.normal_user, slug=sample_skill1.slug)




