from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, UserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Login failed',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'Login successful',
                'data': {
                    'token': token.key,
                    'user': UserSerializer(user).data
                }
            },
            status=status.HTTP_200_OK
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                'message': 'User profile retrieved successfully',
                'data': UserSerializer(request.user).data
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
        except Exception:
            pass

        return Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_200_OK
        )
