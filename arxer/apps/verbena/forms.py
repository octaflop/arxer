from verbena.models import Organization
from django.forms import ModelForm

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization


