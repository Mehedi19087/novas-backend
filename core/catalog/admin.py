from django.contrib import admin
from .models import Category, Product, ProductSpecification, Vessel


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'sort_order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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
class VesselAdmin(admin.ModelAdmin):
    list_display = ('name', 'vessel_id', 'vessel_type', 'length_overall', 'max_speed', 'delivery_lead_time')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'vessel_id', 'vessel_type', 'description')
