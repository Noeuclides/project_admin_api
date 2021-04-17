from apps.users.serializers.base import UserModelSerializer
from apps.users.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.serializers.operator import AccountVerificationSerializer, OperatorRegisterSerializer
from .base import BaseViewSet

class OperatorViewSet(BaseViewSet):
    queryset = User.objects.filter(is_admin=False)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation, now you can create some projects'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch', 'put'])
    def info(self, request, username):
        """Operator register by admin"""
        user = self.get_object()
        serializer = OperatorRegisterSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)