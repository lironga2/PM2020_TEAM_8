from django import forms
from .models import ReportOnHazard


class HazardReportForm(forms.ModelForm):
    hazard_kind = [
        ('מפגע בטיחותי', 'מפגע בטיחותי'),
        ('מפגע תברואתי', 'מפגע תברואתי'),
        ('מפגע אחזקתי', 'מפגע אחזקתי'),
        ('מפגע בציוד', 'מפגע בציוד'),
        ('מפגע אחר', 'מפגע אחר'),
    ]

    report_title = forms.ChoiceField(choices=hazard_kind)
    report_text = forms.Textarea()

    class Meta:
        model = ReportOnHazard
        fields = [
            'report_title',
            'report_text'
        ]
