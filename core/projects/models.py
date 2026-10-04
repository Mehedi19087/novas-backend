from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Active', 'Active'),
        ('Delivered', 'Delivered'),
    ]

    CATEGORY_CHOICES = [
        ('defence', 'Defence'),
        ('maritime', 'Maritime'),
        ('industry', 'Industry'),
        ('consultancy', 'Consultancy'),
        ('geospatial', 'Geospatial'),
    ]

    project_id = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    sector_name = models.CharField(max_length=150)
    client = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    year = models.CharField(max_length=20)
    image_file = models.ImageField(upload_to='novas/projects/', blank=True, null=True, help_text="Upload image to Cloudinary")
    image = models.CharField(max_length=500, blank=True, default='', help_text="Direct image URL or auto-populated from Cloudinary upload")
    summary = models.TextField()
    description = models.TextField()
    features = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Delivered')
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', '-year', 'title']

    def __str__(self):
        return f"[{self.category}] {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image_file:
            try:
                url = self.image_file.url
                if self.image != url:
                    self.image = url
                    super().save(update_fields=['image'])
            except Exception:
                pass



class ProjectSpec(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='specs')
    label = models.CharField(max_length=150)
    value = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.project.title} - {self.label}: {self.value}"
