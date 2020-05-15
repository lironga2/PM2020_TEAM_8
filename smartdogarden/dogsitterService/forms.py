from django import forms
from dogsitterService.models import ActivityTimeDogSitter, MeetingsActivity


class ActivityTimeDogSitterForm(forms.ModelForm):
    activity_date = forms.DateInput()
    activity_start = forms.TimeInput()
    activity_end = forms.TimeInput()

    class Meta:
        model = ActivityTimeDogSitter
        fields = [
            'activity_date',
            'activity_start',
            'activity_end'
        ]


class UpdateMeetingActivity(forms.ModelForm):
    #activity_date = forms.DateInput()
    activity_start = forms.TimeInput()
    activity_end = forms.TimeInput()

    class Meta:
        model = MeetingsActivity
        fields = [
            #'activity_date',
            'activity_start',
            'activity_end'
        ]