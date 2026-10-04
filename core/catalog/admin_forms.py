from django import forms
from core.admin_forms import LinesField, MethodologyField, UploadedImageAdminForm
from .models import Product


class ProductAdminForm(UploadedImageAdminForm):
    certifications = LinesField(label='Certifications')

    class Meta:
        model = Product
        fields = '__all__'


from .models import Vessel


class VesselAdminForm(UploadedImageAdminForm):
    features = LinesField(label='Vessel features')

    class Meta:
        model = Vessel
        fields = '__all__'
