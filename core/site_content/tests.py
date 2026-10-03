from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CompanyProfile, CompanyPillar, BlueprintStep, HeroBannerSlide


class SiteContentAPITestCase(APITestCase):
    def setUp(self):
        self.profile = CompanyProfile.objects.create(
            name="Nova Solutions BD",
            tagline="Excellence in technology",
            mission="Empower defense",
            vision="Global leader"
        )
        self.pillar = CompanyPillar.objects.create(
            pillar_id="commitment",
            keyword="COMMITMENT",
            title="BEST COMMITMENT",
            description="Excellence",
            icon="Handshake"
        )
        self.slide = HeroBannerSlide.objects.create(
            page_identifier="projects",
            title="Tactical Interceptor Craft",
            image_url="/assets/hero/hero-maritime.jpg",
            alignment="left"
        )

    def test_get_company_overview(self):
        url = reverse('company-overview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("profile", response.data["data"])
        self.assertIn("pillars", response.data["data"])

    def test_get_hero_banners_filtered(self):
        url = f"{reverse('hero-banner-list-create')}?page=projects"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["alignment"], "left")
