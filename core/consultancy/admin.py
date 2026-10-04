from core.admin_forms import ContentAdmin
from .admin_forms import ConsultancyServiceAdminForm
from django.contrib import admin
from .models import ConsultancyCategory, ConsultancyService


@admin.register(ConsultancyCategory)
class ConsultancyCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Consultancy category', {'fields': ('name', 'slug', 'category_id')}),
        ('Category description', {'fields': ('tagline', 'description', 'icon_name')}),
        ('Display order', {'fields': ('sort_order',)}),
    )
    list_display = ('name', 'category_id', 'slug', 'sort_order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category_id', 'tagline')


@admin.register(ConsultancyService)
class ConsultancyServiceAdmin(ContentAdmin):
    form = ConsultancyServiceAdminForm
    exclude = ('category_name',)
    autocomplete_fields = ('category',)
    list_select_related = ('category',)
    fieldsets = (
        ('Service and consultancy category', {'fields': ('name', 'slug', 'service_id', 'category')}),
        ('Service image', {'fields': ('image_file', 'image_preview', 'image_url'), 'description': 'Upload an image from your computer. The uploaded file takes priority over the optional image URL.'}),
        ('Service description', {'fields': ('tagline', 'summary', 'description')}),
        ('Scope and delivery', {'fields': ('deliverables', 'target_clients', 'methodology', 'standards', 'duration', 'lead_advisors')}),
        ('Visibility and order', {'fields': ('featured', 'sort_order')}),
    )
    list_display = ('name', 'service_id', 'category', 'duration', 'featured', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'service_id', 'summary', 'description')
    list_filter = ('category', 'featured')
