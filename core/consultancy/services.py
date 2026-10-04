from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import ConsultancyCategory, ConsultancyService


def create_consultancy_category(validated_data: dict) -> ConsultancyCategory:
    """
    Creates a ConsultancyCategory instance with database integrity handling.
    """
    try:
        return ConsultancyCategory.objects.create(**validated_data)
    except IntegrityError as e:
        error_message = str(e).lower()
        if 'category_id' in error_message:
            raise ValidationError({"category_id": "A category with this ID already exists."})
        if 'slug' in error_message:
            raise ValidationError({"slug": "A category with this slug already exists."})
        raise ValidationError({"non_field_errors": ["Could not create consultancy category due to database constraints."]})


def create_consultancy_service(validated_data: dict) -> ConsultancyService:
    """
    Creates a ConsultancyService instance linking it to its category.
    """
    cat_id_or_slug = validated_data.pop('category_id')
    try:
        category = ConsultancyCategory.objects.filter(category_id=cat_id_or_slug).first()
        if not category:
            category = ConsultancyCategory.objects.filter(slug=cat_id_or_slug).first()
        if not category:
            raise ValidationError({"category_id": "Consultancy category does not exist."})
    except Exception:
        raise ValidationError({"category_id": "Invalid consultancy category identifier."})

    if not validated_data.get('category_name'):
        validated_data['category_name'] = category.name

    try:
        return ConsultancyService.objects.create(category=category, **validated_data)
    except IntegrityError as e:
        error_message = str(e).lower()
        if 'service_id' in error_message:
            raise ValidationError({"service_id": "A service with this ID already exists."})
        if 'slug' in error_message:
            raise ValidationError({"slug": "A service with this slug already exists."})
        raise ValidationError({"non_field_errors": ["Could not create consultancy service due to database constraints."]})


from core.content_services import update_content


def update_consultancy_service(service, validated_data):
    data = dict(validated_data)
    if 'category_id' in data:
        key = data.pop('category_id')
        category = ConsultancyCategory.objects.filter(category_id=key).first() or ConsultancyCategory.objects.filter(slug=key).first()
        if not category:
            raise ValidationError({'category_id': 'Consultancy category does not exist.'})
        data['category'] = category
    data['category_name'] = data.get('category', service.category).name
    return update_content(service, data)
