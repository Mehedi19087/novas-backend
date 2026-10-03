from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project


class ProjectsAPITestCase(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(
            project_id="naval-interceptor",
            slug="naval-interceptor",
            title="Naval Interceptor Craft",
            category="maritime",
            sector_name="Maritime",
            client="Coast Guard",
            location="Chittagong",
            year="2024",
            image="/assets/hero/hero-maritime.jpg",
            summary="High speed boat",
            description="Detailed description",
            status="Delivered"
        )

    def test_list_projects(self):
        url = reverse('project-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_filter_projects_by_category(self):
        url = f"{reverse('project-list-create')}?category=maritime"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

        url_empty = f"{reverse('project-list-create')}?category=geospatial"
        response_empty = self.client.get(url_empty)
        self.assertEqual(len(response_empty.data["data"]), 0)
