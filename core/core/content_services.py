from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError


def update_content(instance, validated_data, spec_model=None, spec_parent=None):
    data = dict(validated_data)
    specs = data.pop('specs', None)
    try:
        with transaction.atomic():
            # URL uploads replace the old file reference without deleting shared media.
            image_key = 'image' if hasattr(instance, 'image') else 'image_url'
            if image_key in data and data[image_key] != getattr(instance, image_key, ''):
                instance.image_file = None
            for field, value in data.items():
                setattr(instance, field, value)
            instance.save()
            if specs is not None and spec_model:
                instance.specs.all().delete()
                spec_model.objects.bulk_create([
                    spec_model(**{spec_parent: instance}, **item) for item in specs
                ])
            instance._prefetched_objects_cache = {}
            return instance
    except IntegrityError as exc:
        for field in ('slug', 'sku', 'service_id', 'project_id', 'vessel_id'):
            if field in str(exc).lower():
                raise ValidationError({field: 'An entry with this value already exists.'}) from exc
        raise ValidationError({'detail': 'These changes conflict with an existing record.'}) from exc


def delete_content(instance):
    try:
        with transaction.atomic():
            instance.delete()
    except IntegrityError as exc:
        raise ValidationError({'detail': 'This entry is still referenced by other records.'}) from exc
