from django.db import models


class Sector(models.Model):
    sector_id = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    headline = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default='Shield')
    accent_color = models.CharField(max_length=50, default='#f59e0b')
    capabilities = models.JSONField(default=list, blank=True)
    target_operators = models.JSONField(default=list, blank=True)
    compliance_standards = models.JSONField(default=list, blank=True)
    image_url = models.CharField(max_length=500, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name
