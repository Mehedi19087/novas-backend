from core.admin_forms import ContentAdmin
from .admin_forms import SectorAdminForm
from django.contrib import admin
from .models import Sector


@admin.register(Sector)
class SectorAdmin(ContentAdmin):
    form = SectorAdminForm
    list_filter = ('sector_id',)
    fieldsets = (
        ('Defence, Industry and other sectors', {'fields': ('name', 'slug', 'sector_id')}),
        ('Sector image', {'fields': ('image_file', 'image_preview', 'image_url'), 'description': 'Upload an image from your computer. The uploaded file takes priority over the optional image URL.'}),
        ('Sector overview', {'fields': ('headline', 'tagline', 'description')}),
        ('Sector capabilities', {'fields': ('capabilities', 'target_operators', 'compliance_standards')}),
        ('Appearance and order', {'fields': ('icon_name', 'accent_color', 'sort_order')}),
    )
    list_display = ('name', 'sector_id', 'slug', 'headline', 'accent_color', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sector_id', 'headline', 'description')
