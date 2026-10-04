from django import forms
from core.admin_forms import LinesField, MethodologyField, UploadedImageAdminForm
from .models import ConsultancyService


class ConsultancyServiceAdminForm(UploadedImageAdminForm):
    deliverables = LinesField(label='Scope and deliverables')
    target_clients = LinesField(label='Target clients')
    standards = LinesField(label='Standards')
    methodology = MethodologyField()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.category_name = instance.category.name
        if commit:
            instance.save()
            self.save_m2m()
        return instance

    class Meta:
        model = ConsultancyService
        fields = '__all__'
