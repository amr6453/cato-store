from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile
from .serializers_profile import UserProfileSerializer


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        return self.retrieve(request)
