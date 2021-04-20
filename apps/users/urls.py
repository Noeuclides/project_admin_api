from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import admin, base, operator

router = DefaultRouter()
router.register(r'admin', admin.AdminViewSet, basename='admins')
router.register(r'operator', operator.OperatorViewSet, basename='operators')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', base.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
