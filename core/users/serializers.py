from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone',
            'first_name', 'last_name',
            'is_staff', 'is_superuser'
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username', '').strip()
        password = attrs.get('password', '')

        if not username or not password:
            raise serializers.ValidationError('Both username and password are required.')

        user = authenticate(username=username, password=password)

        # Allow login by email as well if username wasn't matched directly
        if not user and '@' in username:
            try:
                matched_user = User.objects.get(email__iexact=username)
                user = authenticate(username=matched_user.username, password=password)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass

        if not user:
            raise serializers.ValidationError('Invalid username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        attrs['user'] = user
        return attrs


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
    folder = serializers.ChoiceField(
        choices=['novas/uploads', 'novas/products', 'novas/vessels', 'novas/projects', 'novas/consultancy'],
        default='novas/uploads',
    )

    def validate_image(self, image):
        if image.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('Images must be 10 MB or smaller.')
        if image.image.format not in ('JPEG', 'PNG', 'WEBP', 'GIF'):
            raise serializers.ValidationError('Choose a JPG, PNG, WebP or GIF image.')
        return image
