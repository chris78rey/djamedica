from django import forms

from .models import Specialty


class SpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ("name", "description", "is_active")
