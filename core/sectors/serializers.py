from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Sector


class CreateSectorSerializer(serializers.Serializer):
    sector_id = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=Sector.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(queryset=Sector.objects.all())]
    )
    name = serializers.CharField(max_length=150)
    headline = serializers.CharField(max_length=255)
    tagline = serializers.CharField(max_length=255)
    description = serializers.CharField()
    icon_name = serializers.CharField(max_length=50, required=False, default='Shield')
    accent_color = serializers.CharField(max_length=50, required=False, default='#f59e0b')
    capabilities = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    target_operators = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    compliance_standards = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    image_url = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
    sort_order = serializers.IntegerField(required=False, default=0)


class ResponseSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = [
            'id', 'sector_id', 'slug', 'name', 'headline', 'tagline',
            'description', 'icon_name', 'accent_color', 'capabilities',
            'target_operators', 'compliance_standards', 'image_url',
            'sort_order', 'created_at', 'updated_at'
        ]
