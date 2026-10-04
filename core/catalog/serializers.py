from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Category, Product, ProductSpecification, Vessel


# --- Category Serializers ---

class CreateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    description = serializers.CharField(required=False, allow_blank=True, default='')
    icon = serializers.CharField(required=False, allow_blank=True, max_length=50, default='')
    is_active = serializers.BooleanField(required=False, default=True)
    sort_order = serializers.IntegerField(required=False, default=0)


class UpdateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=100)
    slug = serializers.SlugField(required=False, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    icon = serializers.CharField(required=False, allow_blank=True, max_length=50)
    is_active = serializers.BooleanField(required=False)
    sort_order = serializers.IntegerField(required=False)


class ResponseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active', 'sort_order', 'created_at']


# --- Product Specification Serializer ---

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['id', 'label', 'value', 'sort_order']


# --- Product Serializers ---

class CreateProductSpecItemSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=150)
    value = serializers.CharField(max_length=255)
    sort_order = serializers.IntegerField(required=False, default=0)


class CreateProductSerializer(serializers.Serializer):
    sku = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Product.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=150,
        validators=[UniqueValidator(queryset=Product.objects.all())]
    )
    name = serializers.CharField(max_length=255)
    category_id = serializers.IntegerField()
    sector_id = serializers.CharField(max_length=50, required=False, default='defence')
    tagline = serializers.CharField(required=False, allow_blank=True, max_length=255, default='')
    description = serializers.CharField()
    featured = serializers.BooleanField(required=False, default=False)
    certifications = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    specs = CreateProductSpecItemSerializer(many=True, required=False, default=list)
    lead_time = serializers.CharField(required=False, allow_blank=True, max_length=100, default='')
    origin = serializers.CharField(required=False, allow_blank=True, max_length=100, default='')
    warranty = serializers.CharField(required=False, allow_blank=True, max_length=100, default='')
    image_url = serializers.URLField(required=False, allow_blank=True, default='')


class ResponseProductSerializer(serializers.ModelSerializer):
    category = ResponseCategorySerializer(read_only=True)
    specs = ProductSpecificationSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'slug', 'name', 'category', 'sector_id',
            'tagline', 'description', 'featured', 'certifications',
            'specs', 'lead_time', 'origin', 'warranty', 'image_url',
            'created_at', 'updated_at'
        ]

    def get_image_url(self, obj):
        if obj.image_file:
            try:
                return obj.image_file.url
            except Exception:
                pass
        return obj.image_url or ''


# --- Vessel Serializers ---

class CreateVesselSerializer(serializers.Serializer):
    vessel_id = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Vessel.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(queryset=Vessel.objects.all())]
    )
    name = serializers.CharField(max_length=255)
    vessel_type = serializers.CharField(max_length=150)
    tagline = serializers.CharField(required=False, allow_blank=True, max_length=255, default='')
    description = serializers.CharField()
    length_overall = serializers.CharField(max_length=50)
    beam = serializers.CharField(max_length=50)
    draft = serializers.CharField(max_length=50)
    max_speed = serializers.CharField(max_length=50)
    bollard_pull = serializers.CharField(required=False, allow_blank=True, max_length=50, default='')
    engine_power = serializers.CharField(max_length=100)
    hull_material = serializers.CharField(max_length=100)
    classification_society = serializers.CharField(max_length=100)
    crew_capacity = serializers.IntegerField(required=False, default=1)
    delivery_lead_time = serializers.CharField(max_length=100)
    image_url = serializers.URLField(required=False, allow_blank=True, default='')
    features = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )


class ResponseVesselSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Vessel
        fields = [
            'id', 'vessel_id', 'slug', 'name', 'vessel_type', 'tagline',
            'description', 'length_overall', 'beam', 'draft', 'max_speed',
            'bollard_pull', 'engine_power', 'hull_material',
            'classification_society', 'crew_capacity', 'delivery_lead_time',
            'image_url', 'features', 'created_at', 'updated_at'
        ]

    def get_image_url(self, obj):
        if obj.image_file:
            try:
                return obj.image_file.url
            except Exception:
                pass
        return obj.image_url or ''

