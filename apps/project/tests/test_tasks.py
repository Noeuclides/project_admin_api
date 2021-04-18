from apps.project.models import Project, Task
import os
import json
import re
from django.core.management import call_command
from django.test import TestCase
from django.urls.base import reverse
from apps.users.models import User
from django.core import mail
from rest_framework.authtoken.models import Token

from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import datetime
import pytz
from django.core import serializers


class TestProject(TestCase):

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
        self.client = APIClient()
        self.client.post('/api/admin/signup/', self.admin, format='json')
        self.client.post(
            '/api/admin/login/', self.admin_credentials, format='json')
        token = Token.objects.get(user__username=self.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # admin creates an operator
        self.client.post('/api/admin/operator/', self.operator, format='json')

        # get token
        token_regex = '(?<=)(\w.+)(?=\n *<\/code>)'
        token = re.findall(token_regex, mail.outbox[0].body)
        auth_token = {
            'token': token[0]
        }

        # operator verifies account
        self.client_operator = APIClient()

        self.client_operator.post('/api/operator/verify/',
                                  auth_token, format='json')

        # Operator Login
        self.username = self.operator.get('username')
        self.password = self.operator.get('password')
        self.operator_credentials = {
            'username': self.username,
            'password': self.password
        }
        self.client_operator.post(
            '/api/operator/login/', self.operator_credentials, format='json')
        token = Token.objects.get(user__username=self.username)
        self.client_operator.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key)
        operator = User.objects.filter(username=self.username).first()
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
        self.client_operator.post('/api/project/',
                                  self.project, format='json')
        project = Project.objects.filter(
            name=self.project.get('name')).first()
        self.task = {
            'project': project.id,
            'name': 'Task number 1',
            'description': 'This is a test task',
            'execution_date': datetime(2021, 3, 29, tzinfo=pytz.UTC),
        }
        self.task_updated = {
            'project': project.id,
            'name': 'Task number 1 updated',
            'description': 'This is a test task',
            'execution_date': datetime(2021, 4, 10, tzinfo=pytz.UTC),
        }
        return super().setUp()

    def test_task_creation(self):
        response = self.client_operator.post('/api/task/',
                                  self.task, format='json')
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(task.project.id, self.task.get('project'))

    def test_task_update_destroy(self):
        self.client_operator.post('/api/task/',
                                  self.task, format='json')
        response = self.client_operator.put('/api/task/1/',
                                            self.task_updated, format='json')
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.name, self.task_updated.get('name'))
        self.client_operator.delete('/api/task/1/', format='json')
        tasks = Task.objects.all().count()
        self.assertEqual(tasks, 0)

    def test_task_complete(self):
        self.client_operator.post('/api/task/',
                                  self.task, format='json')
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(task.is_complete, False)
        response = self.client_operator.patch('/api/task/1/done/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(task.is_complete, True)

    def test_project_complete_with_send_email_to_admins(self):
        self.client_operator.post('/api/task/',
                                  self.task, format='json')
        self.client_operator.patch('/api/project/1/done/', format='json')
        project = Project.objects.filter(pk=1).first()
        self.assertEqual(project.is_complete, False)

        self.client_operator.patch('/api/task/1/done/', format='json')
        response = self.client_operator.patch('/api/project/1/done/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = Project.objects.filter(pk=1).first()
        self.assertEqual(project.is_complete, True)
        admins = User.objects.filter(is_admin=True).count()
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            print()
            print(mail.outbox)
            print(mail.outbox[0].__dir__())
            print(mail.outbox[0].to)
            print(mail.outbox[1].to)
            self.assertEqual(len(mail.outbox), admins)
            print(mail.outbox[0])

        
       
