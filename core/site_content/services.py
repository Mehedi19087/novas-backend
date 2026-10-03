from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import HeroBannerSlide


def create_hero_banner_slide(validated_data: dict) -> HeroBannerSlide:
    """
    Creates a HeroBannerSlide instance with error handling.
    """
    try:
        return HeroBannerSlide.objects.create(**validated_data)
    except IntegrityError as e:
        raise ValidationError({"non_field_errors": [f"Could not create banner slide: {str(e)}"]})
