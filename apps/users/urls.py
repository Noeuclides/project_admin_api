# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import admin, operator

router = DefaultRouter()
router.register(r'admin', admin.AdminViewSet, basename='admins')
router.register(r'operator', operator.OperatorViewSet, basename='operators')

urlpatterns = [
    path('', include(router.urls))
]
