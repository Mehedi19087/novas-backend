from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Product, Vessel


class CatalogAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Tactical Defense",
            slug="tactical-defense",
            icon="Shield",
            sort_order=1
        )
        self.product = Product.objects.create(
            sku="MK-TEST",
            slug="mk-test",
            name="Test Tactical Helmet",
            category=self.category,
            sector_id="defence",
            description="Testing armor helmet",
            featured=True,
            certifications=["NIJ III"]
        )

    def test_list_categories(self):
        url = reverse('category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertGreaterEqual(len(response.data["data"]), 1)

    def test_create_category(self):
        self.client.force_authenticate(get_user_model().objects.create_user(username="editor", is_staff=True))
        url = reverse('category-list-create')
        data = {
            "name": "New Agriculture",
            "slug": "new-agriculture",
            "description": "Smart tractors and sensors",
            "icon": "Wheat",
            "sort_order": 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["slug"], "new-agriculture")

    def test_list_products(self):
        url = reverse('product-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["data"]), 1)

    def test_get_product_detail(self):
        url = reverse('product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["sku"], "MK-TEST")
