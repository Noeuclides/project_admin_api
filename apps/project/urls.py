from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='projects')
router.register(r'task', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls))
]
