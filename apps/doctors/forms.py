from django import forms

from apps.users.models import User
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = (
            "user",
            "specialty",
            "professional_license",
            "phone",
            "office",
            "bio",
            "is_available",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        used_user_ids = Doctor.objects.exclude(pk=self.instance.pk).values_list("user_id", flat=True)

        qs = User.objects.filter(role=User.Role.DOCTOR).exclude(id__in=used_user_ids)

        if self.instance and self.instance.pk:
            qs = qs | User.objects.filter(pk=self.instance.user_id)

        self.fields["user"].queryset = qs.distinct().order_by(
            "last_name", "first_name", "username"
        )
