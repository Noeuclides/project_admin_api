from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.users.serializers.base import UserModelSerializer
from apps.users.serializers.admin import AdminRegisterSerializer
from .base import BaseViewSet
from apps.users.serializers.operator import OperatorRegisterSerializer


class AdminViewSet(BaseViewSet):

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
