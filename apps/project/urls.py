# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='projects')
router.register(r'task', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls))
]
