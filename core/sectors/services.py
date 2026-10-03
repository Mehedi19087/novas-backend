from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import Sector


def create_sector(validated_data: dict) -> Sector:
    """
    Creates a Sector instance with database constraint handling.
    """
    try:
        return Sector.objects.create(**validated_data)
    except IntegrityError as e:
        error_message = str(e).lower()
        if 'sector_id' in error_message:
            raise ValidationError({"sector_id": "A sector with this ID already exists."})
        if 'slug' in error_message:
            raise ValidationError({"slug": "A sector with this slug already exists."})
        raise ValidationError({"non_field_errors": ["Could not create sector due to database constraints."]})
