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


class ImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        import cloudinary.uploader
        file_obj = request.FILES.get('image') or request.FILES.get('file')
        if not file_obj:
            return Response(
                {'message': 'No image file provided in request.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        folder = request.data.get('folder', 'novas/uploads')

        try:
            upload_result = cloudinary.uploader.upload(
                file_obj,
                folder=folder,
                resource_type='image'
            )
            return Response(
                {
                    'message': 'Image uploaded successfully to Cloudinary',
                    'data': {
                        'url': upload_result.get('secure_url'),
                        'public_id': upload_result.get('public_id'),
                        'format': upload_result.get('format'),
                        'bytes': upload_result.get('bytes'),
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'message': f'Cloudinary upload failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

