from apps.users.models import User
from apps.users.serializers.base import (UserModelSerializer,
                                         UserPasswordChangeSerializer,
                                         UserLoginSerializer)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class BaseViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserModelSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        if self.action in ['password']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

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


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
