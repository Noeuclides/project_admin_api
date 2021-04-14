from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.serializers.operator import AccountVerificationSerializer
from .base import BaseViewSet


class OperatorViewSet(BaseViewSet):

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation, now you can create some projects'}
        return Response(data, status=status.HTTP_200_OK)
