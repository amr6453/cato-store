from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from .serializers import RegisterSerializer, LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user_id': user.pk})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email required'}, status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # don't reveal whether email exists
            return Response({'detail': 'If the email exists, a reset link will be sent.'})

        token = default_token_generator.make_token(user)
        # construct a simple reset link for dev (frontend should handle routing)
        reset_link = f"http://localhost:8000/reset-password/?uid={user.pk}&token={token}"
        subject = 'Password reset for Cato-Store'
        message = render_to_string('users/password_reset_email.txt', {'reset_link': reset_link, 'user': user})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response({'detail': 'If the email exists, a reset link will be sent.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        if not (uid and token and new_password):
            return Response({'detail': 'uid, token and new_password are required'}, status=400)
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid uid'}, status=400)
        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired token'}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password updated'})
