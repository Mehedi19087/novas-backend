from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError
from .models import Category, Product, ProductSpecification, Vessel


def create_category(validated_data: dict) -> Category:
    """
    Creates a Category instance with database integrity handling.
    """
    try:
        return Category.objects.create(**validated_data)
    except IntegrityError as e:
        error_message = str(e).lower()
        if 'name' in error_message:
            raise ValidationError({"name": "A category with this name already exists."})
        if 'slug' in error_message:
            raise ValidationError({"slug": "A category with this slug already exists."})
        raise ValidationError({"non_field_errors": ["Could not create category due to database constraints."]})


def update_category(category: Category, validated_data: dict) -> Category:
    """
    Updates an existing Category instance.
    """
    try:
        for field, value in validated_data.items():
            setattr(category, field, value)
        category.save()
        return category
    except IntegrityError as e:
        error_message = str(e).lower()
        if 'name' in error_message:
            raise ValidationError({"name": "A category with this name already exists."})
        if 'slug' in error_message:
            raise ValidationError({"slug": "A category with this slug already exists."})
        raise ValidationError({"non_field_errors": ["Could not update category due to database constraints."]})


def create_product(validated_data: dict) -> Product:
    """
    Creates a Product instance and associated specifications inside an atomic transaction.
    """
    specs_data = validated_data.pop('specs', [])
    category_id = validated_data.pop('category_id')

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise ValidationError({"category_id": "Category does not exist."})

    try:
        with transaction.atomic():
            product = Product.objects.create(category=category, **validated_data)
            spec_objects = [
                ProductSpecification(
                    product=product,
                    label=item.get('label', ''),
                    value=item.get('value', ''),
                    sort_order=item.get('sort_order', idx)
                )
                for idx, item in enumerate(specs_data)
            ]
            if spec_objects:
                ProductSpecification.objects.bulk_create(spec_objects)
            return product
    except IntegrityError as e:
        error_message = str(e).lower()
        if 'sku' in error_message:
            raise ValidationError({"sku": "A product with this SKU already exists."})
        if 'slug' in error_message:
            raise ValidationError({"slug": "A product with this slug already exists."})
        raise ValidationError({"non_field_errors": ["Could not create product due to database constraints."]})


def create_vessel(validated_data: dict) -> Vessel:
    """
    Creates a Vessel instance with database integrity handling.
    """
    try:
        return Vessel.objects.create(**validated_data)
    except IntegrityError as e:
        error_message = str(e).lower()
        if 'vessel_id' in error_message:
            raise ValidationError({"vessel_id": "A vessel with this ID already exists."})
        if 'slug' in error_message:
            raise ValidationError({"slug": "A vessel with this slug already exists."})
        raise ValidationError({"non_field_errors": ["Could not create vessel due to database constraints."]})


from core.content_services import update_content


def update_product(product, validated_data):
    data = dict(validated_data)
    if 'category_id' in data:
        try:
            data['category'] = Category.objects.get(pk=data.pop('category_id'))
        except Category.DoesNotExist:
            raise ValidationError({'category_id': 'Category does not exist.'})
    return update_content(product, data, ProductSpecification, 'product')


def update_vessel(vessel, validated_data):
    return update_content(vessel, validated_data)
