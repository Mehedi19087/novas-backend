from rest_framework import serializers
from .models import CompanyProfile, CompanyPillar, BlueprintStep, HeroBannerSlide


class ResponseCompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            'id', 'name', 'short_name', 'founder', 'founder_title',
            'founder_image', 'founded_year', 'founded_month', 'team_size',
            'tagline', 'subheading', 'address', 'phone', 'landline',
            'email', 'corporate_registry', 'mission', 'vision', 'values',
            'shipyard_capacity', 'certifications', 'updated_at'
        ]


class ResponseCompanyPillarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPillar
        fields = ['id', 'pillar_id', 'badge', 'keyword', 'title', 'description', 'icon', 'sort_order']


class ResponseBlueprintStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueprintStep
        fields = ['id', 'step', 'title', 'description', 'sort_order']


class CreateHeroBannerSlideSerializer(serializers.Serializer):
    page_identifier = serializers.ChoiceField(choices=HeroBannerSlide.PAGE_CHOICES)
    title = serializers.CharField(max_length=255)
    subtitle = serializers.CharField(required=False, allow_blank=True, default='')
    badge = serializers.CharField(required=False, allow_blank=True, max_length=100, default='')
    image_url = serializers.CharField(max_length=500)
    alignment = serializers.ChoiceField(choices=HeroBannerSlide.ALIGNMENT_CHOICES, required=False, default='left')
    cta_label = serializers.CharField(required=False, allow_blank=True, max_length=100, default='')
    cta_link = serializers.CharField(required=False, allow_blank=True, max_length=255, default='')
    sort_order = serializers.IntegerField(required=False, default=0)
    is_active = serializers.BooleanField(required=False, default=True)


class ResponseHeroBannerSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBannerSlide
        fields = [
            'id', 'page_identifier', 'title', 'subtitle', 'badge',
            'image_url', 'alignment', 'cta_label', 'cta_link',
            'sort_order', 'is_active', 'created_at', 'updated_at'
        ]
