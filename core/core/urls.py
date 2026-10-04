from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 routes
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/catalog/', include('catalog.urls')),
    path('api/v1/consultancy/', include('consultancy.urls')),
    path('api/v1/projects/', include('projects.urls')),
    path('api/v1/sectors/', include('sectors.urls')),
    path('api/v1/content/', include('site_content.urls')),
    path('api/v1/inquiries/', include('inquiries.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
