from django.contrib.admin.models import User
from verbena.models import Organization, Grant, Project, ActionGroup, Member,\
    Workshop, VolunteerOpportunity, Faculty, Student, Location,\
    Event, Member, Research, StudentProject
from photologue.models import Photo
from django.forms import ModelForm
import django.forms as forms
from django.forms.formsets import formset_factory
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from ajax_select.fields import AutoCompleteSelectField

class AvatarForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ('',)

class ProjectForm(ModelForm):
    class Meta:
        model = StudentProject
        exclude = ('approval_status','date_applied','progress_status','portrait','student_leader','professor',)

class EventForm(ModelForm):
    class Meta:
        model = Event

class LocationForm(ModelForm):
    class Meta:
        model = Location

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    passconf = forms.CharField(widget=forms.PasswordInput(),
            label=_("Please confirm your password"))
    email = forms.EmailField()

class MemberForm(ModelForm):
    class Meta:
        model = Member

class MemberForm(ModelForm):
    class Meta:
        model = Member

class FacultyForm(ModelForm):
    class Meta:
        model = Faculty

class StudentForm(ModelForm):
    class Meta:
        model = Student

class VolunteerOpForm(ModelForm):
    class Meta:
        model = VolunteerOpportunity

class WorkshopForm(ModelForm):
    class Meta:
        model = Workshop

class ResearchForm(ModelForm):
    class Meta:
        model = Research

class OrganizationForm(ModelForm):
    """Form for adding new organizations, user is the logged-in user by
    default"""

    class Meta:
        model = Organization
        exclude = ('location','user',)
        fields = ('title', 'slug', 'about', 'mandate',
                'community','service', 'funding', 'annual_budget',
                'nonprofit_status', 'website',)

class ActionGroupForm(ModelForm):
    class Meta:
        model = ActionGroup
        fields =('title', 'slug',)

class GrantForm(ModelForm):
    class Meta:
        model = Grant
        exclude = ('date_applied','approval_status',)

