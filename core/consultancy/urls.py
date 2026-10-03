from django.urls import path
from .views import (
    ConsultancyCategoryListCreateAPIView,
    ConsultancyCategoryDetailAPIView,
    ConsultancyServiceListCreateAPIView,
    ConsultancyServiceDetailAPIView,
)

urlpatterns = [
    path('categories/', ConsultancyCategoryListCreateAPIView.as_view(), name='consultancy-category-list-create'),
    path('categories/<slug:slug>/', ConsultancyCategoryDetailAPIView.as_view(), name='consultancy-category-detail'),
    path('services/', ConsultancyServiceListCreateAPIView.as_view(), name='consultancy-service-list-create'),
    path('services/<slug:slug>/', ConsultancyServiceDetailAPIView.as_view(), name='consultancy-service-detail'),
]
