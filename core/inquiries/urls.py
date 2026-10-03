from django.urls import path
from .views import RFQCreateAPIView, ContactMessageCreateAPIView, NewsletterSubscribeAPIView

urlpatterns = [
    path('rfq/', RFQCreateAPIView.as_view(), name='rfq-create'),
    path('contact/', ContactMessageCreateAPIView.as_view(), name='contact-create'),
    path('newsletter/', NewsletterSubscribeAPIView.as_view(), name='newsletter-subscribe'),
]
