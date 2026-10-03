from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import RFQInquiry, ContactMessage, NewsletterSubscription


class InquiriesAPITestCase(APITestCase):
    def test_submit_rfq(self):
        url = reverse('rfq-create')
        data = {
            "organization_name": "Armed Forces Division",
            "department": "Procurement Bureau",
            "contact_name": "Commander Rahman",
            "email": "procurement@forces.gov.bd",
            "phone": "+8801700000000",
            "delivery_port": "Chittagong Port",
            "timeframe": "60 Days",
            "end_user_confirmed": True,
            "items": [
                {
                    "name": "Ballistic Helmet Mk-III",
                    "category": "Defence",
                    "quantity": 250
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RFQInquiry.objects.count(), 1)
        rfq = RFQInquiry.objects.first()
        self.assertTrue(rfq.reference_id.startswith("RFQ-"))
        self.assertEqual(rfq.items.count(), 1)

    def test_submit_contact_message(self):
        url = reverse('contact-create')
        data = {
            "full_name": "Capt. Zahir",
            "email": "zahir@maritime.com",
            "phone": "+8801811111111",
            "subject": "Tugboat Inquiry",
            "message": "We need specs for TB-3200."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_newsletter_subscribe(self):
        url = reverse('newsletter-subscribe')
        data = {"email": "subscriber@domain.com"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsletterSubscription.objects.count(), 1)
