from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.project.models import Project, Task
from apps.project.serializers import (ProjectModelSerializer,
                                           TaskModelSerializer)
from apps.users.models import User


class ProjectViewSet(viewsets.ModelViewSet):
    """Project view set."""
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer

    @action(detail=True, methods=['patch'])
    def done(self, request, pk):
        task = Task.objects.filter(project__id=pk, is_complete=False)
        if not task:
            data = {
                'message': 'Project done'
            }
            project = Project.objects.filter(
                pk=pk).select_related('user').first()
            project.is_complete = True
            project.save()
            self.send_project_complete_email(project)
        else:
            data = {
                'message': 'You have some tasks missing'
            }
        return Response(data, status=status.HTTP_200_OK)

    def send_project_complete_email(self, project):
        """
        Send account verification link to new operator.
        """
        subject = f'{project} from {project.user} was completed.'
        from_email = 'Project Creator <noreply@projectcreator.com>'
        content = render_to_string(
            'project/project_complete.html',
            {'project': project}
        )
        admins = User.objects.filter(
            is_admin=True).values_list('email', flat=True)
        print(admins)
        msg = EmailMultiAlternatives(
            subject, content, from_email, admins)
        msg.attach_alternative(content, "text/html")
        msg.send()


class TaskViewSet(viewsets.ModelViewSet):
    """Task view set."""
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer

    @action(detail=True, methods=['patch'])
    def done(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        task.is_complete = True
        task.save()
        data = {
            'message': 'Task done'
        }
        return Response(data, status=status.HTTP_200_OK)
