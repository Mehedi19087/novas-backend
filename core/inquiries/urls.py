from .admin_views import InquiryAdminListAPIView, InquiryAdminDetailAPIView
from django.urls import path
from .views import RFQCreateAPIView, ContactMessageCreateAPIView, NewsletterSubscribeAPIView

urlpatterns = [
    path('admin/<str:kind>/', InquiryAdminListAPIView.as_view(), name='inquiry-admin-list'),
    path('admin/<str:kind>/<int:pk>/', InquiryAdminDetailAPIView.as_view(), name='inquiry-admin-detail'),
    path('rfq/', RFQCreateAPIView.as_view(), name='rfq-create'),
    path('contact/', ContactMessageCreateAPIView.as_view(), name='contact-create'),
    path('newsletter/', NewsletterSubscribeAPIView.as_view(), name='newsletter-subscribe'),
]
