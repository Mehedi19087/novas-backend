from django.contrib import admin
from .models import RFQInquiry, RFQItem, ContactMessage, NewsletterSubscription


class RFQItemInline(admin.TabularInline):
    model = RFQItem
    extra = 0


@admin.register(RFQInquiry)
class RFQInquiryAdmin(admin.ModelAdmin):
    list_display = ('reference_id', 'organization_name', 'contact_name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reference_id', 'organization_name', 'contact_name', 'email', 'tender_ref_number')
    readonly_fields = ('reference_id', 'created_at', 'updated_at')
    inlines = [RFQItemInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
