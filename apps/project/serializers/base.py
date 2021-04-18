from apps.users.models import User
from apps.project.models import Project, Task
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from apps.users.serializers.base import UserModelSerializer


class ProjectModelSerializer(serializers.ModelSerializer):

    # user = UserModelSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'user',
            'name',
            'description',
            'start_date',
            'end_date',
        ]

    def validate(self, attrs):
        if attrs.get('start_date') > attrs.get('end_date'):
            raise serializers.ValidationError(
                'End date must be after start date.')
        return attrs


class TaskModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'project',
            'name',
            'description',
            'execution_date',
        ]

    def validate(self, attrs):
        project_start_date = attrs.get('project').start_date
        project_end_date = attrs.get('project').end_date
        execution_date = attrs.get('execution_date')
        if not project_start_date < execution_date < project_end_date:
            raise serializers.ValidationError(
                'Execution date must be between start and end date of the project.')
        return attrs
