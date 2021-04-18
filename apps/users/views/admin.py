from apps.users.models import User
from apps.users.serializers.admin import AdminRegisterSerializer
from apps.users.serializers.base import UserModelSerializer
from apps.users.serializers.operator import OperatorRegisterSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .base import BaseViewSet


class AdminViewSet(BaseViewSet):
    queryset = User.objects.filter(is_admin=True)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        if self.action in ['operator']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """Admin sign up."""
        serializer = AdminRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def operator(self, request):
        """Operator register by admin"""
        serializer = OperatorRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
