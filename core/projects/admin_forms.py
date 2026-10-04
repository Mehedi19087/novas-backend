from django import forms
from core.admin_forms import LinesField, MethodologyField
from .models import Project


class ProjectAdminForm(forms.ModelForm):
    features = LinesField(label='Project highlights')

    class Meta:
        model = Project
        fields = '__all__'
