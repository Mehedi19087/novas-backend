from io import BytesIO
from unittest.mock import patch
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='editor', email='editor@example.com', password='test-password', is_staff=True)

    def test_login_username_email_profile_and_logout(self):
        for identifier in ['editor', 'EDITOR@example.com']:
            response = self.client.post(reverse('auth-login'), {'username': identifier, 'password': 'test-password'})
            self.assertEqual(response.status_code, 200)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['data']['token'])
            self.assertEqual(self.client.get(reverse('auth-me')).data['data']['id'], self.user.id)
            self.assertEqual(self.client.post(reverse('auth-logout')).status_code, 200)
            self.assertEqual(self.client.get(reverse('auth-me')).status_code, 401)
            self.client.credentials()

    def test_invalid_and_disabled_accounts(self):
        url = reverse('auth-login')
        self.assertEqual(self.client.post(url, {'username': 'editor', 'password': 'wrong'}).status_code, 400)
        self.user.is_active = False
        self.user.save()
        self.assertEqual(self.client.post(url, {'username': 'editor', 'password': 'test-password'}).status_code, 400)
        self.assertEqual(self.client.get(reverse('auth-me')).status_code, 401)


class ImageUploadTests(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(username='admin', is_staff=True)
        self.url = reverse('auth-upload')

    def image(self):
        data = BytesIO()
        Image.new('RGB', (2, 2)).save(data, 'PNG')
        return SimpleUploadedFile('test.png', data.getvalue(), content_type='image/png')

    @patch('users.services.cloudinary.uploader.upload')
    def test_permissions(self, upload):
        self.assertEqual(self.client.post(self.url, {'image': self.image()}).status_code, 401)
        user = get_user_model().objects.create_user(username='visitor')
        self.client.force_authenticate(user)
        self.assertEqual(self.client.post(self.url, {'image': self.image()}).status_code, 403)
        upload.assert_not_called()

    @patch('users.services.cloudinary.uploader.upload')
    def test_valid_image_and_legacy_file_field(self, upload):
        upload.return_value = {'secure_url': 'https://example.com/image.png', 'public_id': 'novas/test', 'format': 'png', 'bytes': 80}
        self.client.force_authenticate(self.admin)
        for field in ['image', 'file']:
            response = self.client.post(self.url, {field: self.image(), 'folder': 'novas/products'})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['data']['url'], upload.return_value['secure_url'])
        self.assertEqual(upload.call_args.kwargs['resource_type'], 'image')

    @patch('users.services.cloudinary.uploader.upload')
    def test_invalid_uploads(self, upload):
        self.client.force_authenticate(self.admin)
        cases = [{}, {'image': SimpleUploadedFile('fake.png', b'not an image', content_type='image/png')}, {'image': self.image(), 'folder': '../outside'}]
        large = self.image()
        large.size = 10 * 1024 * 1024 + 1
        # Serializer-level size check avoids allocating an oversized request in the test.
        from .serializers import ImageUploadSerializer
        self.assertFalse(ImageUploadSerializer(data={'image': large}).is_valid())
        for data in cases:
            self.assertEqual(self.client.post(self.url, data).status_code, 400)
        upload.assert_not_called()

    @patch('users.services.cloudinary.uploader.upload')
    def test_provider_failure_does_not_report_success_or_leak_details(self, upload):
        self.client.force_authenticate(self.admin)
        upload.side_effect = RuntimeError('private-provider-detail')
        response = self.client.post(self.url, {'image': self.image()})
        self.assertEqual(response.status_code, 502)
        self.assertNotIn('private-provider-detail', str(response.data))
        upload.side_effect = None
        upload.return_value = {}
        self.assertEqual(self.client.post(self.url, {'image': self.image()}).status_code, 502)
