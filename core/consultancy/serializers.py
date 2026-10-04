from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import ConsultancyCategory, ConsultancyService


class CreateConsultancyCategorySerializer(serializers.Serializer):
    category_id = serializers.CharField(
        max_length=50,
        validators=[UniqueValidator(queryset=ConsultancyCategory.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(queryset=ConsultancyCategory.objects.all())]
    )
    name = serializers.CharField(max_length=150)
    tagline = serializers.CharField(max_length=255)
    description = serializers.CharField()
    icon_name = serializers.CharField(max_length=50, required=False, default='Globe2')
    sort_order = serializers.IntegerField(required=False, default=0)


class ResponseConsultancyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultancyCategory
        fields = [
            'id', 'category_id', 'slug', 'name', 'tagline',
            'description', 'icon_name', 'sort_order', 'created_at'
        ]


class CreateConsultancyServiceSerializer(serializers.Serializer):
    service_id = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=ConsultancyService.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=150,
        validators=[UniqueValidator(queryset=ConsultancyService.objects.all())]
    )
    name = serializers.CharField(max_length=255)
    category_id = serializers.CharField(max_length=50)  # category_id string or pk
    category_name = serializers.CharField(max_length=150, required=False, default='')
    tagline = serializers.CharField(max_length=255)
    summary = serializers.CharField()
    description = serializers.CharField()
    deliverables = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    target_clients = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    methodology = serializers.ListField(required=False, default=list)
    standards = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    duration = serializers.CharField(max_length=100, required=False, default='')
    lead_advisors = serializers.CharField(max_length=255, required=False, default='')
    image_url = serializers.URLField(required=False, allow_blank=True, default='')
    featured = serializers.BooleanField(required=False, default=False)
    sort_order = serializers.IntegerField(required=False, default=0)


class ResponseConsultancyServiceSerializer(serializers.ModelSerializer):
    category = ResponseConsultancyCategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ConsultancyService
        fields = [
            'id', 'service_id', 'slug', 'name', 'category', 'category_name',
            'tagline', 'summary', 'description', 'deliverables',
            'target_clients', 'methodology', 'standards', 'duration',
            'lead_advisors', 'image_url', 'featured', 'sort_order',
            'created_at', 'updated_at'
        ]

    def get_image_url(self, obj):
        if obj.image_file:
            try:
                return obj.image_file.url
            except Exception:
                pass
        return obj.image_url or ''



class UpdateConsultancyServiceSerializer(CreateConsultancyServiceSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not field.required and isinstance(field, serializers.CharField):
                field.allow_blank = True
