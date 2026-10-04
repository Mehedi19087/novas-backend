from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import RFQInquiry, RFQItem, ContactMessage, NewsletterSubscription


class AdminInboxTests(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(username='admin', is_staff=True)
        self.user = get_user_model().objects.create_user(username='visitor')
        self.rfq = RFQInquiry.objects.create(organization_name='Test company', department='Procurement', contact_name='Test sender', email='sender@example.com', phone='123', delivery_port='Dhaka', timeframe='30 days', notes='Private request')
        RFQItem.objects.create(rfq=self.rfq, item_name='Equipment', category='Industry', quantity=3)
        self.contact = ContactMessage.objects.create(full_name='Message sender',email='message@example.com',subject='Question',message='Private message')
        self.subscriber = NewsletterSubscription.objects.create(email='subscriber@example.com')
        self.cases = [('rfq', self.rfq, {'status':'contacted'}), ('contact',self.contact,{'is_read':True}), ('newsletter',self.subscriber,{'is_active':False})]

    def test_private_inboxes_require_staff_for_all_operations(self):
        for user in (None,self.user):
            self.client.force_authenticate(user)
            for kind, item, update in self.cases:
                listing=reverse('inquiry-admin-list',kwargs={'kind':kind})
                detail=reverse('inquiry-admin-detail',kwargs={'kind':kind,'pk':item.pk})
                for response in (self.client.get(listing),self.client.get(detail),self.client.patch(detail,update,format='json'),self.client.delete(detail)):
                    self.assertIn(response.status_code,(401,403))
                    self.assertNotIn('Private',str(response.data))
        self.assertEqual(RFQInquiry.objects.count(),1)

    def test_admin_reads_updates_filters_and_deletes_all_types(self):
        self.client.force_authenticate(self.admin)
        for kind,item,update in self.cases:
            listing=reverse('inquiry-admin-list',kwargs={'kind':kind})
            detail=reverse('inquiry-admin-detail',kwargs={'kind':kind,'pk':item.pk})
            response=self.client.get(listing)
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.data['data']['count'],1)
            self.assertEqual(self.client.get(detail).data['data']['email'],item.email)
            response=self.client.patch(detail,update,format='json')
            self.assertEqual(response.status_code,200,response.data)
            item.refresh_from_db()
            key,value=next(iter(update.items()))
            self.assertEqual(getattr(item,key),value)
            self.assertEqual(self.client.get(listing,{'status':str(value).lower()}).data['data']['count'],1)
            self.assertEqual(self.client.patch(detail,{'email':'changed@example.com'},format='json').status_code,400)
            self.assertEqual(self.client.delete(detail).status_code,204)
            self.assertEqual(self.client.get(detail).status_code,404)
        self.assertFalse(RFQItem.objects.exists())

    def test_rfq_items_search_validation_and_pagination(self):
        self.client.force_authenticate(self.admin)
        url=reverse('inquiry-admin-list',kwargs={'kind':'rfq'})
        data=self.client.get(url,{'search':self.rfq.reference_id}).data['data']
        self.assertEqual(data['results'][0]['items'][0]['quantity'],3)
        self.assertEqual(self.client.get(url,{'search':'missing'}).data['data']['count'],0)
        self.assertEqual(self.client.get(url,{'status':'invalid'}).status_code,400)
        detail=reverse('inquiry-admin-detail',kwargs={'kind':'rfq','pk':self.rfq.pk})
        self.assertEqual(self.client.patch(detail,{'status':'invalid'},format='json').status_code,400)
        self.assertEqual(self.client.get(reverse('inquiry-admin-list',kwargs={'kind':'unknown'})).status_code,404)
        contact_url=reverse('inquiry-admin-list',kwargs={'kind':'contact'})
        self.assertEqual(self.client.get(contact_url, {'search':f'INQ-{self.contact.pk}'}).data['data']['count'],1)
        NewsletterSubscription.objects.bulk_create([NewsletterSubscription(email=f'item{i}@example.com') for i in range(26)])
        url=reverse('inquiry-admin-list',kwargs={'kind':'newsletter'})
        first=self.client.get(url).data['data'];second=self.client.get(url,{'page':2}).data['data']
        self.assertEqual(first['count'],27)
        self.assertEqual(len(first['results']),25)
        self.assertEqual(len(second['results']),2)
        self.assertFalse(set(x['id'] for x in first['results']) & set(x['id'] for x in second['results']))
