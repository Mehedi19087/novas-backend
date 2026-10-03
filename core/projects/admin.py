from django.contrib import admin
from .models import Project, ProjectSpec


class ProjectSpecInline(admin.TabularInline):
    model = ProjectSpec
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'location', 'year', 'status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'client', 'location', 'summary')
    list_filter = ('category', 'status', 'is_featured', 'year')
    inlines = [ProjectSpecInline]
