from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    icon = models.CharField(max_length=50, blank=True, default='')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sector_id = models.CharField(max_length=50, default='defence')
    tagline = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    featured = models.BooleanField(default=False)
    certifications = models.JSONField(default=list, blank=True)
    lead_time = models.CharField(max_length=100, blank=True, default='')
    origin = models.CharField(max_length=100, blank=True, default='')
    warranty = models.CharField(max_length=100, blank=True, default='')
    image_url = models.URLField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', 'name']

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specs')
    label = models.CharField(max_length=150)
    value = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.product.name} - {self.label}: {self.value}"


class Vessel(models.Model):
    vessel_id = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    vessel_type = models.CharField(max_length=150)
    tagline = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField()
    length_overall = models.CharField(max_length=50)
    beam = models.CharField(max_length=50)
    draft = models.CharField(max_length=50)
    max_speed = models.CharField(max_length=50)
    bollard_pull = models.CharField(max_length=50, blank=True, default='')
    engine_power = models.CharField(max_length=100)
    hull_material = models.CharField(max_length=100)
    classification_society = models.CharField(max_length=100)
    crew_capacity = models.PositiveIntegerField(default=1)
    delivery_lead_time = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500)
    features = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
