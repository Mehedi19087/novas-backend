from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError
from .models import Project, ProjectSpec


def create_project(validated_data: dict) -> Project:
    """
    Creates a Project and associated specs atomically with error handling.
    """
    specs_data = validated_data.pop('specs', [])

    try:
        with transaction.atomic():
            project = Project.objects.create(**validated_data)
            spec_objects = [
                ProjectSpec(
                    project=project,
                    label=item.get('label', ''),
                    value=item.get('value', ''),
                    sort_order=item.get('sort_order', idx)
                )
                for idx, item in enumerate(specs_data)
            ]
            if spec_objects:
                ProjectSpec.objects.bulk_create(spec_objects)
            return project
    except IntegrityError as e:
        error_message = str(e).lower()
        if 'project_id' in error_message:
            raise ValidationError({"project_id": "A project with this ID already exists."})
        if 'slug' in error_message:
            raise ValidationError({"slug": "A project with this slug already exists."})
        raise ValidationError({"non_field_errors": ["Could not create project due to database constraints."]})


from core.content_services import update_content


def update_project(project, validated_data):
    return update_content(project, validated_data, ProjectSpec, 'project')
