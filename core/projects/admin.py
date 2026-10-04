from core.admin_forms import ContentAdmin
from .admin_forms import ProjectAdminForm
from django.contrib import admin
from .models import Project, ProjectSpec


class ProjectSpecInline(admin.TabularInline):
    model = ProjectSpec
    extra = 1


@admin.register(Project)
class ProjectAdmin(ContentAdmin):
    form = ProjectAdminForm
    image_url_field = 'image'
    list_editable = ('priority',)
    fieldsets = (
        ('Display priority', {'fields': ('priority',)}),
        ('Project and category', {'fields': ('title', 'slug', 'project_id', 'category', 'sector_name')}),
        ('Project image', {'fields': ('image_file', 'image_preview', 'image'), 'description': 'Upload an image from your computer. The uploaded file takes priority over the optional image URL.'}),
        ('Project description', {'fields': ('summary', 'description', 'features')}),
        ('Client and delivery', {'fields': ('client', 'location', 'year', 'status')}),
        ('Visibility and order', {'fields': ('is_featured', 'sort_order')}),
    )
    list_display = ('title', 'category', 'client', 'location', 'year', 'status', 'is_featured', 'priority')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'client', 'location', 'summary')
    list_filter = ('category', 'status', 'is_featured', 'year')
    inlines = [ProjectSpecInline]
