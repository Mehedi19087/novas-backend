from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APITestCase
from catalog.models import Category, Product, ProductSpecification, Vessel
from consultancy.models import ConsultancyCategory, ConsultancyService
from projects.models import Project, ProjectSpec


@override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'}, 'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}})
class ContentMutationTests(APITestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(username='editor', is_staff=True)
        self.visitor = get_user_model().objects.create_user(username='visitor')
        self.category = Category.objects.create(name='Equipment', slug='equipment')
        self.product = Product.objects.create(name='Product', slug='product', sku='SKU', category=self.category, description='Original', image_url='https://example.com/old.png', certifications=['Old'], warranty='3 years')
        ProductSpecification.objects.create(product=self.product, label='Old', value='Value')
        self.vessel = Vessel.objects.create(name='Vessel', slug='vessel', vessel_id='V-1', crew_capacity=2)
        self.project = Project.objects.create(title='Project', slug='project', project_id='P-1', category='defence', year='2026')
        ProjectSpec.objects.create(project=self.project, label='Old', value='Value')
        self.consultancy_category = ConsultancyCategory.objects.create(name='Project', slug='project', category_id='project')
        self.service = ConsultancyService.objects.create(name='Service', slug='service', service_id='S-1', category=self.consultancy_category, category_name='Project')
        self.entries = [('product-detail', self.product, 'name'), ('vessel-detail', self.vessel, 'name'), ('project-detail', self.project, 'title'), ('consultancy-service-detail', self.service, 'name')]

    def test_all_types_update_and_delete(self):
        self.client.force_authenticate(self.staff)
        for route, instance, field in self.entries:
            url = reverse(route, kwargs={'slug': instance.slug})
            with self.subTest(route=route):
                response = self.client.patch(url, {field: 'Updated', 'slug': instance.slug}, format='json')
                self.assertEqual(response.status_code, 200, response.data)
                instance.refresh_from_db()
                self.assertEqual(getattr(instance, field), 'Updated')
                self.assertEqual(self.client.delete(url).status_code, 204)
                self.assertFalse(type(instance).objects.filter(pk=instance.pk).exists())
                self.assertEqual(self.client.get(url).status_code, 404)
                self.assertEqual(self.client.delete(url).status_code, 404)
        self.assertFalse(ProductSpecification.objects.exists())
        self.assertFalse(ProjectSpec.objects.exists())

    def test_non_admin_cannot_mutate_any_type(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user)
            for route, instance, field in self.entries:
                url = reverse(route, kwargs={'slug': instance.slug})
                self.assertIn(self.client.patch(url, {field:'Unauthorized'}, format='json').status_code, (401,403))
                self.assertIn(self.client.delete(url).status_code, (401,403))
                self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(Product.objects.get(pk=self.product.pk).name, 'Product')

    def test_product_replaces_specs_and_clears_optional_fields(self):
        self.client.force_authenticate(self.staff)
        url = reverse('product-detail', kwargs={'slug':'product'})
        response = self.client.patch(url, {'specs':[{'label':'Capacity','value':'20'}], 'certifications':[], 'warranty':''}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['data']['specs'][0]['label'], 'Capacity')
        self.assertEqual(self.product.specs.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.image_url, 'https://example.com/old.png')
        self.assertEqual(self.product.warranty, '')
        self.assertEqual(self.product.certifications, [])
        self.assertEqual(self.client.patch(url, {'specs':[]}, format='json').status_code, 200)
        self.assertEqual(self.product.specs.count(), 0)

    def test_invalid_update_does_not_lose_specs_or_image(self):
        Product.objects.create(name='Other', sku='OTHER', slug='other', category=self.category)
        self.client.force_authenticate(self.staff)
        url = reverse('product-detail', kwargs={'slug':'product'})
        for invalid in ({'sku':'OTHER', 'specs':[]}, {'category_id':999999, 'specs':[]}):
            self.assertEqual(self.client.patch(url, invalid, format='json').status_code, 400)
            self.product.refresh_from_db()
            self.assertEqual(self.product.sku, 'SKU')
            self.assertEqual(self.product.specs.count(), 1)

    def test_replacement_image_clears_old_file_reference(self):
        Product.objects.filter(pk=self.product.pk).update(image_file='old.png')
        self.client.force_authenticate(self.staff)
        url = reverse('product-detail', kwargs={'slug':'product'})
        response = self.client.patch(url, {'image_url':'https://example.com/new.png'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.product.refresh_from_db()
        self.assertFalse(self.product.image_file)
        self.assertEqual(response.data['data']['image_url'], 'https://example.com/new.png')

    def test_consultancy_category_and_methodology_change(self):
        category = ConsultancyCategory.objects.create(name='Tender', slug='tender', category_id='tender')
        self.client.force_authenticate(self.staff)
        url = reverse('consultancy-service-detail', kwargs={'slug':'service'})
        response = self.client.patch(url, {'category_id':'tender', 'methodology':[{'step':'01','title':'Review','desc':'Details'}], 'duration':''}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.service.refresh_from_db()
        self.assertEqual(self.service.category, category)
        self.assertEqual(self.service.category_name, 'Tender')
        self.assertEqual(self.service.methodology[0]['title'], 'Review')

    def test_priority_controls_every_content_list_and_can_be_changed(self):
        self.client.force_authenticate(self.staff)
        cases = [
            ('product-list-create', 'product-detail', self.product, 'sku', '?category=equipment&sector=defence'),
            ('vessel-list-create', 'vessel-detail', self.vessel, 'vessel_id', ''),
            ('project-list-create', 'project-detail', self.project, 'project_id', '?category=defence'),
            ('consultancy-service-list-create', 'consultancy-service-detail', self.service, 'service_id', '?category=project'),
        ]
        for list_route, detail_route, original, identifier, query in cases:
            with self.subTest(route=list_route):
                self.assertEqual(original.priority, 100)
                other = type(original).objects.get(pk=original.pk)
                other.pk = None
                other.slug = 'priority-first'
                setattr(other, identifier, 'priority-first')
                if hasattr(other, 'name'): other.name = 'ZZZ priority first'
                if hasattr(other, 'title'): other.title = 'ZZZ priority first'
                other.priority = 1
                other.save()
                url = reverse(list_route) + query
                data = self.client.get(url).data['data']
                self.assertEqual([row['id'] for row in data], [other.pk, original.pk])
                self.assertEqual(data[0]['priority'], 1)
                response = self.client.patch(reverse(detail_route, kwargs={'slug': other.slug}), {'priority': 200}, format='json')
                self.assertEqual(response.status_code, 200, response.data)
                data = self.client.get(url).data['data']
                self.assertEqual([row['id'] for row in data], [original.pk, other.pk])

    def test_invalid_priorities_are_rejected_for_every_content_type(self):
        self.client.force_authenticate(self.staff)
        for route, instance, _ in self.entries:
            for priority in (0, -1, 1.5, 'abc', 2147483648):
                response = self.client.patch(reverse(route, kwargs={'slug':instance.slug}), {'priority':priority}, format='json')
                self.assertEqual(response.status_code, 400, (route, priority, response.data))
                instance.refresh_from_db()
                self.assertEqual(instance.priority, 100)
