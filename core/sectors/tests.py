from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Sector


class SectorsAPITestCase(APITestCase):
    def setUp(self):
        self.sector = Sector.objects.create(
            sector_id="defence",
            slug="defence",
            name="Defence",
            headline="Force Protection",
            tagline="Certified tactical systems",
            description="Novas supplies battle-proven gear",
            icon_name="Shield",
            accent_color="#f59e0b"
        )

    def test_list_sectors(self):
        url = reverse('sector-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_get_sector_detail(self):
        url = reverse('sector-detail', kwargs={'slug': 'defence'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["sector_id"], "defence")
