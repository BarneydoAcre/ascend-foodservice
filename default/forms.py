from django import forms

from . import models


class NewRegisterForm(forms.ModelForm):
    class Meta:
        model = models.NewRegister
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]
        exclude =[
            'created',
            'updated',
        ]

class AddBugReportForm(forms.ModelForm):
    class Meta:
        model = models.BugReport
        fields = [
            'company',
            'company_worker',
            'bug',
        ]
        exclude = []