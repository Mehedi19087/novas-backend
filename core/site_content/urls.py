from django.urls import path
from .views import CompanyOverviewAPIView, HeroBannerSlideListCreateAPIView

urlpatterns = [
    path('company/', CompanyOverviewAPIView.as_view(), name='company-overview'),
    path('hero-banners/', HeroBannerSlideListCreateAPIView.as_view(), name='hero-banner-list-create'),
]
