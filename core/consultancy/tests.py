from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ConsultancyCategory, ConsultancyService


class ConsultancyAPITestCase(APITestCase):
    def setUp(self):
        self.category = ConsultancyCategory.objects.create(
            category_id="international",
            slug="international",
            name="International Consultancy",
            tagline="Global OEM representation",
            description="Connecting international defense OEMs",
            icon_name="Globe2"
        )
        self.service = ConsultancyService.objects.create(
            service_id="oem-representation",
            slug="oem-representation",
            name="OEM Strategic Representation",
            category=self.category,
            category_name="International Consultancy",
            tagline="Tier-1 liaison",
            summary="Strategic entry",
            description="Full lifecycle representation",
            deliverables=["Registration"],
            featured=True
        )

    def test_list_consultancy_categories(self):
        url = reverse('consultancy-category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_list_consultancy_services(self):
        url = reverse('consultancy-service-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_get_consultancy_category_detail(self):
        url = reverse('consultancy-category-detail', kwargs={'slug': 'international'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("services", response.data["data"])
