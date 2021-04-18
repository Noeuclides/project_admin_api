from django.db import models
from django.core.exceptions import ValidationError


class Project(models.Model):
    """Model definition for Project."""

    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    name = models.CharField('Project name', max_length=50, unique=True)
    description = models.TextField('Project description')
    start_date = models.DateTimeField("Start date", auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField("End date", auto_now=False, auto_now_add=False)
    is_complete = models.BooleanField(default=False)


    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """Unicode representation of Project."""
        return f'Project {self.name}'

    def clean(self) -> None:
        if self.start_date < self.end_date:
            raise ValidationError("End date must be after start date.")


class Task(models.Model):
    """Model definition for Task."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField('Task name', max_length=50)
    description = models.TextField('Task decription')
    execution_date = models.DateTimeField('Execution date', auto_now=False, auto_now_add=False)
    is_complete = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Task."""

        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        """Unicode representation of Task."""
        return f'{self.name} from {self.project}'

    def clean(self) -> None:
        if not self.project.start_date < self.execution_date < self.project.end_date:
            raise ValidationError("Execution date must be between start and end date of the project.")

