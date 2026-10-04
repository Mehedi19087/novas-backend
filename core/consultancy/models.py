from django.db import models


class ConsultancyCategory(models.Model):
    category_id = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default='Globe2')
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Consultancy Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class ConsultancyService(models.Model):
    service_id = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        ConsultancyCategory,
        on_delete=models.CASCADE,
        related_name='services'
    )
    category_name = models.CharField(max_length=150)
    tagline = models.CharField(max_length=255)
    summary = models.TextField()
    description = models.TextField()
    deliverables = models.JSONField(default=list, blank=True)
    target_clients = models.JSONField(default=list, blank=True)
    methodology = models.JSONField(default=list, blank=True)
    standards = models.JSONField(default=list, blank=True)
    duration = models.CharField(max_length=100, blank=True, default='')
    lead_advisors = models.CharField(max_length=255, blank=True, default='')
    image_file = models.ImageField(upload_to='novas/consultancy/', blank=True, null=True, help_text="Upload image to Cloudinary")
    image_url = models.URLField(max_length=500, blank=True, default='', help_text="Direct image URL or auto-populated from Cloudinary upload")
    featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', '-featured', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image_file:
            try:
                url = self.image_file.url
                if self.image_url != url:
                    self.image_url = url
                    super().save(update_fields=['image_url'])
            except Exception:
                pass

