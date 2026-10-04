from django import forms
from core.admin_forms import LinesField, MethodologyField
from .models import CompanyProfile


class CompanyProfileAdminForm(forms.ModelForm):
    values = LinesField(label='Company values')
    certifications = LinesField(label='Certifications')

    class Meta:
        model = CompanyProfile
        fields = '__all__'
