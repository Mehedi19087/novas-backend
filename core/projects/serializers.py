from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Project, ProjectSpec


class ProjectSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSpec
        fields = ['id', 'label', 'value', 'sort_order']


class CreateProjectSpecItemSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=150)
    value = serializers.CharField(max_length=255)
    sort_order = serializers.IntegerField(required=False, default=0)


class CreateProjectSerializer(serializers.Serializer):
    project_id = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=Project.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=150,
        validators=[UniqueValidator(queryset=Project.objects.all())]
    )
    title = serializers.CharField(max_length=255)
    category = serializers.ChoiceField(choices=Project.CATEGORY_CHOICES)
    sector_name = serializers.CharField(max_length=150)
    client = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    year = serializers.CharField(max_length=20)
    image = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
    summary = serializers.CharField()
    description = serializers.CharField()
    features = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    specs = CreateProjectSpecItemSerializer(many=True, required=False, default=list)
    status = serializers.ChoiceField(choices=Project.STATUS_CHOICES, required=False, default='Delivered')
    is_featured = serializers.BooleanField(required=False, default=False)
    sort_order = serializers.IntegerField(required=False, default=0)


class ResponseProjectSerializer(serializers.ModelSerializer):
    specs = ProjectSpecSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'project_id', 'slug', 'title', 'category', 'sector_name',
            'client', 'location', 'year', 'image', 'summary', 'description',
            'features', 'specs', 'status', 'is_featured', 'sort_order',
            'created_at', 'updated_at'
        ]

    def get_image(self, obj):
        if obj.image_file:
            try:
                return obj.image_file.url
            except Exception:
                pass
        return obj.image or ''

