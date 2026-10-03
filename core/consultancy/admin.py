from django.contrib import admin
from .models import ConsultancyCategory, ConsultancyService


@admin.register(ConsultancyCategory)
class ConsultancyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'slug', 'sort_order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category_id', 'tagline')


@admin.register(ConsultancyService)
class ConsultancyServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_id', 'category', 'duration', 'featured', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'service_id', 'summary', 'description')
    list_filter = ('category', 'featured')
