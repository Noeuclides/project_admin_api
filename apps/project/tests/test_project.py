from apps.project.models import Project
from rest_framework import status

from .test_base import TestBaseAPI

class TestProject(TestBaseAPI):

    def test_project_creation(self):
        response = self.client_operator.post('/api/project/',
                                             self.project, format='json')
        project = Project.objects.filter(
            name=self.project.get('name')).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(project.user.username, 'first_op')

    def test_project_update_destroy(self):
        self.client_operator.post('/api/project/',
                                  self.project, format='json')

        response = self.client_operator.put('/api/project/1/',
                                            self.project_updated, format='json')
        project = Project.objects.filter(
            name=self.project_updated.get('name')).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(project.name, self.project_updated.get('name'))
        self.client_operator.delete('/api/project/1/',
                                 self.project_updated, format='json')
        projects = Project.objects.all().count()
        self.assertEqual(projects, 0)

    
       