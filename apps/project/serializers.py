from django.db.models import Q
from rest_framework import serializers

from apps.project.models import Project, Task
from apps.users.models import User
from apps.users.serializers.base import UserModelSerializer


class ProjectModelSerializer(serializers.ModelSerializer):

    user = UserModelSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'user',
            'name',
            'description',
            'start_date',
            'end_date',
            'is_complete'
        ]

    def create(self, validated_data):
        user = self.context.get('request').user
        project = Project(**validated_data, user=user)
        project.save()
        return project

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if instance.start_date > instance.end_date:
            raise serializers.ValidationError(
                'End date must be after start date.')
        query_filter = Q(execution_date__lt=instance.start_date) | Q(
            execution_date__gt=instance.end_date)
        tasks = Task.objects.filter(query_filter, project__id=instance.id)
        if tasks:
            raise serializers.ValidationError(
                'Task execution dates must be between start and end date of the project')
        instance.save()
        return instance


class TaskModelSerializer(serializers.ModelSerializer):
    project = ProjectModelSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'project',
            'name',
            'description',
            'execution_date',
            'is_complete'
        ]

    def create(self, validated_data):
        project = self.context.get('project')
        project = Task(**validated_data, project=project)
        project.save()
        return project

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        project_start_date = instance.project.start_date
        project_end_date = instance.project.end_date
        execution_date = instance.execution_date
        if not project_start_date < execution_date < project_end_date:
            raise serializers.ValidationError(
                'Execution date must be between start and end date of the project.')
        instance.save()
        return instance

    def test_serializer(self):
        project = self.project
        return project
