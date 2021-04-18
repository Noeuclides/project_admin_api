import json
import os
import re

import pytz
from apps.project.models import Project, Task
from apps.users.models import User
from django.core import mail, serializers
from django.core.management import call_command
from django.test import TestCase
from django.urls.base import reverse
from django.utils.timezone import datetime
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestBaseAPI(TestCase):

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
        self.admin_credentials = {
            'username': self.username,
            'password': self.password
        }

        # admin signup and login
        self.client = self.admin_apiclient()

        # admin creates an operator
        self.client.post('/api/admin/operator/', self.operator, format='json')

        # get token
        auth_token = self.get_auth_token()

        # operator account verification and login
        self.username_op = self.operator.get('username')
        self.password_op = self.operator.get('password')
        self.operator_credentials = {
            'username': self.username_op,
            'password': self.password_op
        }
        self.client_operator = self.operator_apiclient(auth_token)

        operator = User.objects.filter(username=self.username_op).first()
        self.project = {
            'user': operator.id,
            'name': 'Test_project',
            'description': 'This is a test',
            'start_date': datetime(2021, 3, 21, tzinfo=pytz.UTC),
            'end_date': datetime(2021, 4, 21, tzinfo=pytz.UTC),
        }
        self.project_updated = {
            'user': operator.id,
            'name': 'Test_project_updated',
            'description': 'This is a test',
            'start_date': datetime(2021, 3, 21, tzinfo=pytz.UTC),
            'end_date': datetime(2021, 5, 21, tzinfo=pytz.UTC),
        }

        return super().setUp()

    def admin_apiclient(self):
        client = APIClient()
        client.post('/api/admin/signup/', self.admin, format='json')
        client.post(
            '/api/admin/login/', self.admin_credentials, format='json')
        token = Token.objects.get(user__username=self.username)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    def operator_apiclient(self, auth_token):
        client_operator = APIClient()

        client_operator.post('/api/operator/verify/',
                             auth_token, format='json')

        # Operator Login
        client_operator.post(
            '/api/operator/login/', self.operator_credentials, format='json')
        token = Token.objects.get(user__username=self.username_op)
        client_operator.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key)
        return client_operator

    def get_auth_token(self):
        token_regex = '(?<=)(\w.+)(?=\n *<\/code>)'
        token = re.findall(token_regex, mail.outbox[0].body)
        return {
            'token': token[0]
        }
