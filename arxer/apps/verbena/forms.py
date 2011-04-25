from verbena.models import Organization, Grant, Project, ActionGroup
from django.forms import ModelForm

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization

class ActionGroupForm(ModelForm):
    class Meta:
        model = Organization

class GrantForm(ModelForm):
    class Meta:
        model = Grant
        exclude = ('date_applied','approval_status',)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('approval_status','date_applied','progress_status',)

