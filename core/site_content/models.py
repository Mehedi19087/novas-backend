from django.db import models


class CompanyProfile(models.Model):
    name = models.CharField(max_length=150, default='Nova Solutions BD')
    short_name = models.CharField(max_length=50, default='NOVAS')
    founder = models.CharField(max_length=150, default='Mr. Raoson Alom')
    founder_title = models.CharField(max_length=150, default='Founder & CEO, Novas')
    founder_image = models.CharField(max_length=500, default='/assets/founder.png')
    founded_year = models.CharField(max_length=20, default='2012')
    founded_month = models.CharField(max_length=50, default='July 2012')
    team_size = models.CharField(max_length=150, default='24-member specialized engineering & research team')
    tagline = models.CharField(max_length=255, default='Achieving excellence in the field of science, technology and procurement')
    subheading = models.TextField(blank=True, default='')
    address = models.TextField(default='House No-412, Road No-29, Flat-5A-5B-4B, Mohakhali DOHS, Dhaka, Bangladesh')
    phone = models.CharField(max_length=50, default='+8801711264822')
    landline = models.CharField(max_length=50, blank=True, default='9832552')
    email = models.EmailField(default='info@novasbd.com')
    corporate_registry = models.CharField(max_length=100, default='REG-BD-NOVAS-2012')
    mission = models.TextField()
    vision = models.TextField()
    values = models.JSONField(default=list, blank=True)
    shipyard_capacity = models.JSONField(default=dict, blank=True)
    certifications = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profile'

    def __str__(self):
        return self.name


class CompanyPillar(models.Model):
    pillar_id = models.CharField(max_length=50, unique=True)
    badge = models.CharField(max_length=50, default='BEST')
    keyword = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title


class BlueprintStep(models.Model):
    step = models.CharField(max_length=10)
    title = models.CharField(max_length=150)
    description = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'step']

    def __str__(self):
        return f"{self.step} - {self.title}"


class HeroBannerSlide(models.Model):
    ALIGNMENT_CHOICES = [
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ]

    PAGE_CHOICES = [
        ('home', 'Home'),
        ('projects', 'Projects'),
        ('consultancy', 'Consultancy'),
        ('defence', 'Defence'),
        ('industry', 'Industry'),
        ('maritime', 'Maritime'),
        ('geospatial', 'Geospatial'),
    ]

    page_identifier = models.CharField(max_length=50, choices=PAGE_CHOICES)
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True, default='')
    badge = models.CharField(max_length=100, blank=True, default='')
    image_url = models.CharField(max_length=500)
    alignment = models.CharField(max_length=20, choices=ALIGNMENT_CHOICES, default='left')
    cta_label = models.CharField(max_length=100, blank=True, default='')
    cta_link = models.CharField(max_length=255, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['page_identifier', 'sort_order', 'id']

    def __str__(self):
        return f"[{self.page_identifier}] {self.title} ({self.alignment})"
