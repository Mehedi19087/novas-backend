"""Editor-friendly fields; stored JSON and public API shapes remain unchanged."""
from django import forms
from django.contrib import admin
from django.utils.html import format_html


class LinesField(forms.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault('widget', forms.Textarea(attrs={'rows': 5, 'cols': 80}))
        kwargs.setdefault('help_text', 'Enter one item per line. Leave blank for no items.')
        super().__init__(**kwargs)

    def prepare_value(self, value):
        if isinstance(value, list):
            return '\n'.join(value)
        return value

    def to_python(self, value):
        return [line.strip() for line in (value or '').splitlines() if line.strip()]


class MethodologyField(LinesField):
    def __init__(self, **kwargs):
        kwargs.setdefault('help_text', 'One step per line: step number | title | description. Example: 1 | Discovery | Review the project requirements.')
        super().__init__(**kwargs)

    def prepare_value(self, value):
        if isinstance(value, list):
            return '\n'.join(' | '.join(str(step.get(key, '')) for key in ('step', 'title', 'desc')) for step in value)
        return value

    def to_python(self, value):
        steps = []
        for line in super().to_python(value):
            parts = [part.strip() for part in line.split('|', 2)]
            if len(parts) != 3 or not all(parts):
                raise forms.ValidationError('Each step needs a number, title and description separated by |.')
            steps.append(dict(zip(('step', 'title', 'desc'), parts)))
        return steps


class ContentAdmin(admin.ModelAdmin):
    readonly_fields = ('image_preview',)
    save_on_top = True
    list_per_page = 25
    image_field = 'image_file'
    image_url_field = 'image_url'

    @admin.display(description='Current image')
    def image_preview(self, obj):
        if not obj or not obj.pk:
            return 'Save an image upload to see its preview.'
        uploaded = getattr(obj, self.image_field, None)
        url = uploaded.url if uploaded else getattr(obj, self.image_url_field, '')
        if not url:
            return 'No image uploaded.'
        return format_html('<img src="{}" alt="Current image" style="max-width:320px;max-height:180px;object-fit:contain">', url)


class UploadedImageAdminForm(forms.ModelForm):
    image_url = forms.CharField(required=False, help_text='Optional external image URL. An uploaded image takes priority.')

    def clean_image_url(self):
        value = self.cleaned_data.get('image_url', '')
        uploaded = self.cleaned_data.get('image_file')
        # Model.save() synchronizes this value after storing the uploaded file.
        # Do not validate a storage-generated relative URL as an external URL.
        if uploaded and self.instance.pk and self.instance.image_file:
            if value == self.instance.image_file.url:
                return ''
        return forms.URLField(required=False).clean(value)
