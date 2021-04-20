from django.test import TestCase
from apps.users.models import User
from django.core import mail

from rest_framework.test import APIClient
from rest_framework import status


class TestAdmin(TestCase):

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
        self.client = APIClient()

        return super().setUp()

    def test_admin_signup(self):
        client = APIClient()
        response = client.post('/api/admin/signup/', self.admin, format='json')
        user = User.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('username'), user.username)
        self.assertEqual(user.is_admin, True)

    def test_admin_login(self):
        self.client.post('/api/admin/signup/', self.admin, format='json')
        login_credentials = {
            'username': self.admin.get('username'),
            'password': self.admin.get('password')
        }
        response = self.client.post(
            '/api/login/', login_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAdminActions(TestCase):

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

    def test_operator_creation(self):
        response = self.client.post('/api/admin/operator/',
                                    self.operator, format='json')
        user = User.objects.filter(
            username=self.operator.get('username')).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_enabled, False)

    def test_send_confirmation_email(self):
        self.client.post('/api/admin/operator/', self.operator, format='json')
        user = User.objects.filter(username='first_op').first()
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].to[0], user.email)

    def test_admin_change_password(self):
        user = User.objects.get(username=self.username)
        password_change = {
            'new_password': 'newpassadmin',
            'confirm_new_password': 'newpassadmin',
            'password': self.admin.get('password'),
        }

        response = self.client.post(
            '/api/admin/password/', password_change, format='json')
        user_updated = User.objects.get(username=self.username)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user_updated.password, user.password)

    def test_admin_update_operator(self):
        response = self.client.post('/api/admin/operator/',
                                    self.operator, format='json')
        user = User.objects.filter(
            username=self.operator.get('username')).first()
        self.assertEqual(user.is_enabled, False)
        self.operator['is_enabled'] = True
        response = self.client.put(
            f'/api/operator/{user.id}/', self.operator, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_updated = User.objects.filter(
            id=user.id).first()
        self.assertEqual(user_updated.is_enabled, True)
