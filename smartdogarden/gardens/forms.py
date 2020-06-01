from django import forms
from .models import ReportOnHazard, HazardReports


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


class UpdateHazardReportStatus(forms.ModelForm):
    hazard_status = [
        ('נמצא בטיפול', 'נמצא בטיפול'),
        ('טופל', 'טופל'),
        ('Not yet addressed', 'Not yet addressed'),
    ]

    report_status = forms.ChoiceField(choices=hazard_status)

    class Meta:
        model = HazardReports
        fields = [
            'report_status'
        ]
