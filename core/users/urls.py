from django.urls import path
from .views import LoginView, MeView, LogoutView, ImageUploadAPIView

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('me/', MeView.as_view(), name='auth-me'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('upload/', ImageUploadAPIView.as_view(), name='auth-upload'),
]
