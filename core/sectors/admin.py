from django.contrib import admin
from .models import Sector


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector_id', 'slug', 'headline', 'accent_color', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sector_id', 'headline', 'description')
