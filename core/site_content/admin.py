from core.admin_forms import ContentAdmin
from .admin_forms import CompanyProfileAdminForm
from django.contrib import admin
from .models import CompanyProfile, CompanyPillar, BlueprintStep, HeroBannerSlide


@admin.register(CompanyProfile)
class CompanyProfileAdmin(ContentAdmin):
    form = CompanyProfileAdminForm
    image_field = 'founder_image_file'
    image_url_field = 'founder_image'
    fieldsets = (
        ('Company identity', {'fields': ('name', 'short_name', 'tagline', 'subheading', 'founded_year', 'founded_month', 'team_size', 'corporate_registry')}),
        ('Founder', {'fields': ('founder', 'founder_title', 'founder_image_file', 'image_preview', 'founder_image')}),
        ('Contact information', {'fields': ('address', 'phone', 'landline', 'email')}),
        ('About the company', {'fields': ('mission', 'vision', 'values', 'certifications', 'shipyard_capacity')}),
    )
    list_display = ('name', 'founder', 'email', 'phone', 'founded_year')


@admin.register(CompanyPillar)
class CompanyPillarAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Company pillar', {'fields': ('pillar_id', 'title', 'description', 'badge', 'keyword', 'icon')}),
        ('Display order', {'fields': ('sort_order',)}),
    )
    list_display = ('title', 'pillar_id', 'badge', 'keyword', 'icon', 'sort_order')


@admin.register(BlueprintStep)
class BlueprintStepAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Process step', {'fields': ('step', 'title', 'description')}),
        ('Display order', {'fields': ('sort_order',)}),
    )
    list_display = ('step', 'title', 'sort_order')


@admin.register(HeroBannerSlide)
class HeroBannerSlideAdmin(ContentAdmin):
    fieldsets = (
        ('Page and banner text', {'fields': ('page_identifier', 'title', 'subtitle', 'badge')}),
        ('Banner image', {'fields': ('image_file', 'image_preview', 'image_url'), 'description': 'Upload an image from your computer. The uploaded file takes priority over the optional image URL.'}),
        ('Button', {'fields': ('cta_label', 'cta_link')}),
        ('Layout and visibility', {'fields': ('alignment', 'sort_order', 'is_active')}),
    )
    list_display = ('title', 'page_identifier', 'alignment', 'sort_order', 'is_active')
    list_filter = ('page_identifier', 'alignment', 'is_active')
    search_fields = ('title', 'subtitle', 'badge')


admin.site.site_header = 'NOVAS Content Administration'
admin.site.site_title = 'NOVAS Admin'
admin.site.index_title = 'Choose a section to manage its categories, details and images'
