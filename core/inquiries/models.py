import uuid
from django.db import models
from django.utils import timezone


class RFQInquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('contacted', 'Contacted Client'),
        ('fulfilled', 'Fulfilled'),
        ('closed', 'Closed'),
    ]

    reference_id = models.CharField(max_length=50, unique=True, editable=False)
    organization_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    tender_ref_number = models.CharField(max_length=100, blank=True, default='')
    delivery_port = models.CharField(max_length=150)
    timeframe = models.CharField(max_length=100)
    end_user_confirmed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'RFQ Inquiry'
        verbose_name_plural = 'RFQ Inquiries'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reference_id:
            date_str = timezone.now().strftime('%Y%m%d')
            unique_suffix = uuid.uuid4().hex[:6].upper()
            self.reference_id = f"RFQ-{date_str}-{unique_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_id} - {self.organization_name}"


class RFQItem(models.Model):
    rfq = models.ForeignKey(RFQInquiry, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item_name} (x{self.quantity})"


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, default='')
    company = models.CharField(max_length=150, blank=True, default='')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.full_name} - {self.subject}"


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
