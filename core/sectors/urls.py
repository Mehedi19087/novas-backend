from django.urls import path
from .views import SectorListCreateAPIView, SectorDetailAPIView

urlpatterns = [
    path('sectors/', SectorListCreateAPIView.as_view(), name='sector-list-create'),
    path('sectors/<slug:slug>/', SectorDetailAPIView.as_view(), name='sector-detail'),
]
