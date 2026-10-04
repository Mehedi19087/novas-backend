from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import RFQInquiry, RFQItem, ContactMessage, NewsletterSubscription


class RFQItemInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=100, required=False, default='')
    quantity = serializers.IntegerField(min_value=1, default=1)


class RFQItemOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = ['id', 'item_name', 'category', 'quantity']


class CreateRFQSerializer(serializers.Serializer):
    organization_name = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=255)
    contact_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=50)
    tender_ref_number = serializers.CharField(required=False, allow_blank=True, max_length=100, default='')
    delivery_port = serializers.CharField(max_length=150)
    timeframe = serializers.CharField(max_length=100)
    end_user_confirmed = serializers.BooleanField(default=False)
    notes = serializers.CharField(required=False, allow_blank=True, default='')
    items = RFQItemInputSerializer(many=True, required=False, default=list)


class ResponseRFQSerializer(serializers.ModelSerializer):
    items = RFQItemOutputSerializer(many=True, read_only=True)

    class Meta:
        model = RFQInquiry
        fields = [
            'id', 'reference_id', 'organization_name', 'department',
            'contact_name', 'email', 'phone', 'tender_ref_number',
            'delivery_port', 'timeframe', 'end_user_confirmed', 'notes',
            'status', 'items', 'created_at'
        ]


class CreateContactMessageSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = serializers.CharField(required=False, allow_blank=True, max_length=50, default='')
    company = serializers.CharField(required=False, allow_blank=True, max_length=150, default='')
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()


class ResponseContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'full_name', 'email', 'phone', 'company', 'subject', 'message', 'is_read', 'created_at']


class CreateNewsletterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=NewsletterSubscription.objects.all(), message="This email is already subscribed.")]
    )


class ResponseNewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['id', 'email', 'is_active', 'subscribed_at']


class UpdateRFQStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=RFQInquiry.STATUS_CHOICES)


class UpdateContactReadSerializer(serializers.Serializer):
    is_read = serializers.BooleanField()


class UpdateSubscriptionSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
