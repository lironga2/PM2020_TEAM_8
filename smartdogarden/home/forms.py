from django import forms
from .models import GardenAdminNotice


class GardenAdminNoticeForm(forms.ModelForm):
    announcement_text = forms.Textarea()

    class Meta:
        model = GardenAdminNotice
        fields = [
                  'announcement_text'
                  ]
