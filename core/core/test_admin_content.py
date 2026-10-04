import tempfile
from io import BytesIO
from PIL import Image
from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.admin_forms import LinesField, MethodologyField
from consultancy.models import ConsultancyCategory, ConsultancyService
from consultancy.serializers import ResponseConsultancyServiceSerializer


@override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'}, 'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class ContentAdminTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_superuser(username='editor', email='editor@example.com', password='test-password'))
        self.category = ConsultancyCategory.objects.create(category_id='project', slug='project', name='Project Consultancy', tagline='Advisory', description='Project services')

    def test_all_content_forms_render(self):
        for model, model_admin in admin.site._registry.items():
            if model._meta.app_label in {'catalog', 'projects', 'consultancy', 'sectors', 'site_content'}:
                with self.subTest(model=model.__name__):
                    response = self.client.get(reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_add'))
                    self.assertEqual(response.status_code, 200)

    def test_consultancy_manual_upload_and_category_change(self):
        buffer = BytesIO()
        Image.new('RGB', (8, 8), color='blue').save(buffer, 'PNG')
        data = dict(name='Engineering advisory', slug='engineering-advisory', service_id='advisory', category=self.category.pk, tagline='Engineering', summary='Service summary', description='Service details', deliverables='Feasibility review\nImplementation plan', target_clients='Shipyards', methodology='01 | Discovery | Review requirements', standards='ISO 9001', duration='6 months', lead_advisors='Engineers', sort_order=0)
        with tempfile.TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            data['image_file'] = SimpleUploadedFile('service.png', buffer.getvalue(), content_type='image/png')
            response = self.client.post(reverse('admin:consultancy_consultancyservice_add'), data)
            self.assertEqual(response.status_code, 302, getattr(response, 'context', None) and response.context['adminform'].form.errors)
            service = ConsultancyService.objects.get(service_id='advisory')
            self.assertEqual(service.category_name, 'Project Consultancy')
            payload = ResponseConsultancyServiceSerializer(service).data
            self.assertEqual(payload['deliverables'], ['Feasibility review', 'Implementation plan'])
            self.assertEqual(payload['methodology'], [{'step':'01', 'title':'Discovery', 'desc':'Review requirements'}])
            self.assertIn('novas/consultancy/', payload['image_url'])
            self.assertTrue(service.image_file.storage.exists(service.image_file.name))
            other = ConsultancyCategory.objects.create(category_id='tender', slug='tender', name='Tender Consultancy', tagline='Tender', description='Tender services')
            data.pop('image_file')
            data['category'] = other.pk
            data['image_url'] = service.image_url
            response = self.client.post(reverse('admin:consultancy_consultancyservice_change', args=[service.pk]), data)
            self.assertEqual(response.status_code, 302, response.context['adminform'].form.errors if response.context else '')
            service.refresh_from_db()
            self.assertEqual(service.category_name, other.name)
            self.assertTrue(service.image_file)

    def test_list_fields_and_invalid_methodology(self):
        field = LinesField()
        self.assertEqual(field.clean(' One\n\n Two '), ['One', 'Two'])
        self.assertEqual(field.clean(''), [])
        self.assertEqual(field.prepare_value(['One', 'Two']), 'One\nTwo')
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            MethodologyField().clean('Missing separators')
