from core.admin_forms import ContentAdmin
from .admin_forms import ProductAdminForm, VesselAdminForm
from django.contrib import admin
from .models import Category, Product, ProductSpecification, Vessel


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Product category', {'fields': ('name', 'slug', 'description', 'icon')}),
        ('Visibility and order', {'fields': ('is_active', 'sort_order')}),
    )
    list_display = ('name', 'slug', 'is_active', 'sort_order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(ContentAdmin):
    form = ProductAdminForm
    autocomplete_fields = ('category',)
    list_select_related = ('category',)
    fieldsets = (
        ('Product and category', {'fields': ('name', 'slug', 'sku', 'category', 'sector_id')}),
        ('Product image', {'fields': ('image_file', 'image_preview', 'image_url'), 'description': 'Upload an image from your computer. The uploaded file takes priority over the optional image URL.'}),
        ('Product description', {'fields': ('tagline', 'description')}),
        ('Supply and certification', {'fields': ('certifications', 'lead_time', 'origin', 'warranty')}),
        ('Homepage visibility', {'fields': ('featured',)}),
    )
    list_display = ('name', 'sku', 'category', 'sector_id', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sku', 'description')
    list_filter = ('category', 'sector_id', 'featured')
    inlines = [ProductSpecificationInline]


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'label', 'value', 'sort_order')
    search_fields = ('product__name', 'label', 'value')


@admin.register(Vessel)
class VesselAdmin(ContentAdmin):
    form = VesselAdminForm
    fieldsets = (
        ('Vessel identity', {'fields': ('name', 'slug', 'vessel_id', 'vessel_type')}),
        ('Vessel image', {'fields': ('image_file', 'image_preview', 'image_url'), 'description': 'Upload an image from your computer. The uploaded file takes priority over the optional image URL.'}),
        ('Vessel description', {'fields': ('tagline', 'description', 'features')}),
        ('Dimensions and performance', {'fields': ('length_overall', 'beam', 'draft', 'max_speed', 'bollard_pull', 'engine_power', 'hull_material', 'classification_society', 'crew_capacity')}),
        ('Delivery', {'fields': ('delivery_lead_time',)}),
    )
    list_display = ('name', 'vessel_id', 'vessel_type', 'length_overall', 'max_speed', 'delivery_lead_time')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'vessel_id', 'vessel_type', 'description')
