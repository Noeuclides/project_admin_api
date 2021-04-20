from apps.users.models import User
from apps.users.serializers.base import UserModelSerializer
from apps.users.serializers.operator import (AccountVerificationSerializer,
                                             OperatorRegisterSerializer)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .base import BaseViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.users.permissions import IsAdmin


class OperatorViewSet(BaseViewSet):
    queryset = User.objects.filter(is_admin=False)
    serializer_class = OperatorRegisterSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        if self.action in ['enable', 'disable']:
            permission_classes = [IsAdmin]
        elif self.action in ['verify']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation, now you can create some projects'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch', 'put'])
    def enable(self, request, pk):
        """Account verification."""
        operator = User.objects.filter(id=pk, is_admin=False).first()
        if not operator:
            data = {'message': f'There is not operator with id {pk}'}
        else:
            operator.is_enabled = True
            operator.save()
            data = {'message': f'Operator {operator} is enabled'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch', 'put'])
    def disable(self, request, pk):
        """Account verification."""
        operator = User.objects.filter(id=pk, is_admin=False).first()
        if not operator:
            data = {'message': f'There is not operator with id {pk}'}
        else:
            operator.is_enabled = False
            operator.save()
            data = {'message': f'Operator {operator} is disabled'}
        return Response(data, status=status.HTTP_200_OK)
