from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError
from .models import RFQInquiry, RFQItem, ContactMessage, NewsletterSubscription


def create_rfq(validated_data: dict) -> RFQInquiry:
    """
    Creates an RFQ and its associated items atomically.
    """
    items_data = validated_data.pop('items', [])

    try:
        with transaction.atomic():
            rfq = RFQInquiry.objects.create(**validated_data)
            item_objects = [
                RFQItem(
                    rfq=rfq,
                    item_name=item.get('name', ''),
                    category=item.get('category', ''),
                    quantity=item.get('quantity', 1)
                )
                for item in items_data
            ]
            if item_objects:
                RFQItem.objects.bulk_create(item_objects)
            return rfq
    except IntegrityError as e:
        raise ValidationError({"non_field_errors": [f"Could not submit RFQ due to database constraints: {str(e)}"]})


def create_contact_message(validated_data: dict) -> ContactMessage:
    """
    Creates a ContactMessage instance.
    """
    try:
        return ContactMessage.objects.create(**validated_data)
    except IntegrityError as e:
        raise ValidationError({"non_field_errors": [f"Could not submit message: {str(e)}"]})


def subscribe_newsletter(validated_data: dict) -> NewsletterSubscription:
    """
    Subscribes an email to the newsletter.
    """
    try:
        return NewsletterSubscription.objects.create(**validated_data)
    except IntegrityError as e:
        raise ValidationError({"email": ["This email address is already subscribed."]})


def update_inquiry_state(instance, validated_data):
    try:
        with transaction.atomic():
            for field, value in validated_data.items():
                setattr(instance, field, value)
            instance.save()
        return instance
    except IntegrityError as exc:
        raise ValidationError({'detail': 'Could not update this submission.'}) from exc


def delete_inquiry(instance):
    try:
        with transaction.atomic():
            instance.delete()
    except IntegrityError as exc:
        raise ValidationError({'detail': 'Could not delete this submission.'}) from exc
