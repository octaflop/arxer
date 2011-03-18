from verbena.models import Organization, Grant
from django.forms import ModelForm

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization

class GrantForm(ModelForm):
    class Meta:
        model = Grant
        exclude = ('approval_status','date_applied',)

