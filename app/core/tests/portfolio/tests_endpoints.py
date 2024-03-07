from django.test import TestCase
from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from users.models import BaseUser
from portfolio.models import (
    Portfolio,
    PortfolioComment
)
from core.services.portfolio import (
    create_portfolio,
    publish_portfolio,
    create_comment,
)
from core.services.users import (
    register,
    create_profile,
)

PORTFOLIO_URL = reverse('portfolio:create_portfolio')
LIST_MY_PORTFOLIOS_URL = reverse('portfolio:my_portfolios')
COMMENT_URL = reverse('portfolio:comment')


class TestPublicEndpoints(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
    
    # def tearDown(self) -> None:
    #     cache.delete_pattern('*')

    def test_create_portfolio_unauthenticated_unsuccessfully(self):
        response = self.client.post(PORTFOLIO_URL, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_portfolios_unauthenticated_unsuccessfully(self):
        response = self.client.get(LIST_MY_PORTFOLIOS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_portfolio_unauthenticated_unsuccessfully(self):
        url = reverse('portfolio:portfolio_detail', args=['test'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_portfolio_unauthenticated_unsuccessfully(self):
        url = reverse('portfolio:portfolio_detail', args=['test'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_comments_with_unauthenticated_user_unsuccessfully(self):
        response = self.client.get(COMMENT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_publish_portfolio_with_unauthenticated_unsuccessfully(self):
        url = reverse('portfolio:publish_portfolio', args=['test'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_create_portfolio_comment_unauthenticated_unsuccessfully(self):
    #     response = self.client.post(COMMENT_URL, {})

    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_portfolio_comment_unauthenticated_unsuccessfully(self):
        url = reverse('portfolio:delete_comment', args=['test'])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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
        response = self.normal_client.post(PORTFOLIO_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Portfolio.objects.filter(title=payload['title']).exists()
        )

    def test_list_my_portfolios_authenticated_successfully(self):
        create_portfolio(
            user=self.admin_user,
            title='Advanced RestFull API',
            description=None,
            cover_image=None
        )
        create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )
        create_portfolio(
            user=self.normal_user,
            title='E-Commerce web service',
            description=None,
            cover_image=None

        )

        response = self.normal_client.get(LIST_MY_PORTFOLIOS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_portfolio_authenticated_successfully(self):
        sample_portfolio = create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )
        url = reverse('portfolio:portfolio_detail', args=[sample_portfolio.slug])
        response = self.normal_client.get(url)
        sample_portfolio.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sample_portfolio.views, 1)

    def test_delete_another_user_portfolio_unsuccessfully(self):
        sample_portfolio1 = create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )
        url = reverse('portfolio:portfolio_detail', args=[sample_portfolio1.slug])
        response = self.admin_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            Portfolio.objects.filter(title=sample_portfolio1.title).exists()
        )


    def test_delete_my_portfolio_successfully(self):
        sample_portfolio1 = create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )
        url = reverse('portfolio:portfolio_detail', args=[sample_portfolio1.slug])
        response = self.normal_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Portfolio.objects.filter(title=sample_portfolio1.title).exists()
        )

    def test_list_comments_by_normal_user_unsuccessfully(self):
        response = self.normal_client.get(COMMENT_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_comments_only_by_admin_user_successfully(self):
        portfolio1 = create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )

        create_comment(
            user=self.admin_user,
            portfolio=portfolio1,
            comment='Example comment1'
        )
        create_comment(
            user=self.normal_user,
            portfolio=portfolio1,
            comment='Example comment2'
        )
        response = self.admin_client.get(COMMENT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_publish_portfolio_with_normal_user_unsuccessfully(self):
        portfolio1 = create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )
        url = reverse('portfolio:publish_portfolio', args=[portfolio1.slug])
        response = self.normal_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_publish_non_existing_portfolio_unsuccessfully(self):
        url = reverse('portfolio:publish_portfolio', args=['wrong-slug'])
        response = self.admin_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_publish_portfolio_with_admin_user_successfully(self):
        portfolio1 = create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )
        url = reverse('portfolio:publish_portfolio', args=[portfolio1.slug])
        response = self.admin_client.get(url)
        portfolio1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(portfolio1.published)

    # def test_create_portfolio_comment_authenticated_successfully(self):
    #     pass

    def test_delete_another_portfolio_comment_authenticated_unsuccessfully(self):
        """
        Test deleting a portfolio which belongs to another user unsuccessfully.
        """
        portfolio1 = create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )
        sample_comment = create_comment(
            user=self.normal_user,
            portfolio=portfolio1,
            comment='Example comment1'
        )
        url = reverse('portfolio:delete_comment', args=[sample_comment.pk])

        response = self.admin_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(PortfolioComment.objects.filter(
            comment=sample_comment.comment
        ).exists())

    def test_delete_my_portfolio_comment_authenticated_successfully(self):
        """
        Test deleting a portfolio which belongs
        to myself another user unsuccessfully.
        """
        portfolio1 = create_portfolio(
            user=self.normal_user,
            title='E-Learning web service',
            description=None,
            cover_image=None
        )
        sample_comment = create_comment(
            user=self.normal_user,
            portfolio=portfolio1,
            comment='Example comment1'
        )
        url = reverse('portfolio:delete_comment', args=[sample_comment.pk])

        response = self.normal_client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PortfolioComment.objects.filter(
            comment=sample_comment.comment
        ).exists())
