import pytz
from apps.project.models import Project, Task
from apps.users.models import User
from django.core import mail
from django.utils.timezone import datetime
from rest_framework import status

from .test_base import TestBaseAPI


class TestTask(TestBaseAPI):

    def setUp(self):
        super().setUp()
        # project creation
        self.client_operator.post('/api/project/',
                                  self.project, format='json')
        # task creation
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
        response = self.client_operator.post('/api/project/1/task/',
                                             self.task, format='json')
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(task.project.id, self.task.get('project'))

    def test_task_update_destroy(self):
        self.client_operator.post('/api/project/1/task/',
                                  self.task, format='json')
        response = self.client_operator.put('/api/project/1/task/1/',
                                            self.task_updated, format='json')
            
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.name, self.task_updated.get('name'))
        self.client_operator.delete('/api/project/1/task/1/', format='json')
        tasks = Task.objects.all().count()
        self.assertEqual(tasks, 0)

    def test_task_complete(self):
        self.client_operator.post('/api/project/1/task/',
                                  self.task, format='json')
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(task.is_complete, False)
        response = self.client_operator.patch(
            f'/api/project/1/task/{task.id}/done/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(task.is_complete, True)

    def test_project_complete_with_send_email_to_admins(self):
        self.client_operator.post('/api/project/1/task/',
                                  self.task, format='json')
        self.client_operator.patch('/api/project/1/done/', format='json')
        project = Project.objects.filter(pk=1).first()
        self.assertEqual(project.is_complete, False)

        self.client_operator.patch('/api/project/1/task/1/done/', format='json')

        response = self.client_operator.patch(
            '/api/project/1/done/', format='json')
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
