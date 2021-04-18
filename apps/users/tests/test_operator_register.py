import re

from apps.users.models import User
from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class BaseTest(TestCase):
    def setUp(self):
        self.admin = {
            'username': 'first_admin',
            'email': 'first_admin@gmail.com',
            'name': 'first',
            'last_name': 'admin',
            'password': 'passadmin',
            'password_confirmation': 'passadmin',
        }
        self.operator = {
            'username': 'first_op',
            'email': 'first_op@gmail.com',
            'name': 'first',
            'last_name': 'op',
            'password': 'operator123',
            'password_confirmation': 'operator123',
            'is_admin': False,
            'is_enabled': False,
        }
        self.username = self.admin.get('username')
        self.password = self.admin.get('password')
        self.login_credentials = {
            'username': self.username,
            'password': self.password
        }
        self.client = APIClient()
        self.client.post('/api/admin/signup/', self.admin, format='json')
        response = self.client.post(
            '/api/login/', self.login_credentials, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        return super().setUp()


class TestOperator(BaseTest):

    def test_verify_account_with_token(self):
        client = APIClient()
        self.client.post('/api/admin/operator/', self.operator, format='json')
        user = User.objects.filter(username='first_op').first()
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_enabled, False)

        # get token
        token_regex = '(?<=)(\w.+)(?=\n *<\/code>)'
        token = re.findall(token_regex, mail.outbox[0].body)
        auth_token = {
            'token': token[0]
        }
        response = client.post('/api/operator/verify/',
                               auth_token, format='json')

        # get user with values updated
        user_updated = User.objects.get(username=user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_updated.is_enabled, True)
