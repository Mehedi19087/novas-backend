from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


class ContentMetadataPermissionsTests(APITestCase):
    routes = ['category-list-create', 'consultancy-category-list-create', 'sector-list-create', 'hero-banner-list-create']

    def test_public_read_and_restricted_write(self):
        regular = get_user_model().objects.create_user(username='reader')
        admin = get_user_model().objects.create_user(username='editor', is_staff=True)
        for route in self.routes:
            with self.subTest(route=route):
                url = reverse(route)
                self.client.force_authenticate(None)
                self.assertEqual(self.client.get(url).status_code, 200)
                self.assertEqual(self.client.post(url, {}, format='json').status_code, 401)
                self.client.force_authenticate(regular)
                self.assertEqual(self.client.post(url, {}, format='json').status_code, 403)
                self.client.force_authenticate(admin)
                # Reaches field validation only after the permission check succeeds.
                self.assertEqual(self.client.post(url, {}, format='json').status_code, 400)

    def test_staff_can_create_metadata_and_read_details(self):
        self.client.force_authenticate(get_user_model().objects.create_user(username='admin', is_staff=True))
        cases = [
            ('category-list-create', 'category-detail', {'name':'Equipment', 'slug':'equipment'}),
            ('consultancy-category-list-create', 'consultancy-category-detail', {'category_id':'advisory', 'slug':'advisory', 'name':'Advisory', 'tagline':'Advice', 'description':'Details'}),
            ('sector-list-create', 'sector-detail', {'sector_id':'industry', 'slug':'industry', 'name':'Industry', 'headline':'Industry', 'tagline':'Services', 'description':'Details'}),
            ('hero-banner-list-create', None, {'page_identifier':'home', 'title':'New banner'}),
        ]
        for route, detail, payload in cases:
            with self.subTest(route=route):
                result = self.client.post(reverse(route), payload, format='json')
                self.assertEqual(result.status_code, 201, result.data)
                self.assertTrue(result.data['data']['id'])
                if detail:
                    url = reverse(detail, kwargs={'slug':payload['slug']})
                    self.assertEqual(self.client.get(url).status_code, 200)
                    self.assertEqual(self.client.get(reverse(detail, kwargs={'slug':'absent'})).status_code, 404)
