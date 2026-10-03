from django.urls import path
from .views import (
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    ProductListCreateAPIView,
    ProductDetailAPIView,
    VesselListCreateAPIView,
    VesselDetailAPIView,
)

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('vessels/', VesselListCreateAPIView.as_view(), name='vessel-list-create'),
    path('vessels/<slug:slug>/', VesselDetailAPIView.as_view(), name='vessel-detail'),
]
