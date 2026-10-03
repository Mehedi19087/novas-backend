from django.contrib import admin
from .models import CompanyProfile, CompanyPillar, BlueprintStep, HeroBannerSlide


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder', 'email', 'phone', 'founded_year')


@admin.register(CompanyPillar)
class CompanyPillarAdmin(admin.ModelAdmin):
    list_display = ('title', 'pillar_id', 'badge', 'keyword', 'icon', 'sort_order')


@admin.register(BlueprintStep)
class BlueprintStepAdmin(admin.ModelAdmin):
    list_display = ('step', 'title', 'sort_order')


@admin.register(HeroBannerSlide)
class HeroBannerSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_identifier', 'alignment', 'sort_order', 'is_active')
    list_filter = ('page_identifier', 'alignment', 'is_active')
    search_fields = ('title', 'subtitle', 'badge')
