from django import forms
from core.admin_forms import LinesField, MethodologyField
from .models import Sector


class SectorAdminForm(forms.ModelForm):
    capabilities = LinesField(label='Capabilities')
    target_operators = LinesField(label='Target operators')
    compliance_standards = LinesField(label='Compliance standards')

    class Meta:
        model = Sector
        fields = '__all__'
