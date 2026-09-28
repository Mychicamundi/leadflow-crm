from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "company", "source", "stage", "value", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}
