from apps.users.models import User
from apps.users.serializers.base import (UserLoginSerializer,
                                         UserModelSerializer, UserPasswordChangeSerializer)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class BaseViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter()
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def password(self, request):
        """User password change."""
        serializer = UserPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user)
        data = {
            'message': 'Password changed'
        }
        return Response(data, status=status.HTTP_200_OK)
