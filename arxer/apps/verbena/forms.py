from verbena.models import Organization, Grant, Project, ActionGroup, Member,\
    Workshop, VolunteerOpportunity
from django.forms import ModelForm
import django.forms as forms
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

class VolunteerOpForm(ModelForm):
    class Meta:
        model = VolunteerOpportunity

class WorkshopForm(ModelForm):
    class Meta:
        model = Workshop

class OrganizationForm(ModelForm):
    """Form for adding new organizations, user is the logged-in user by
    default"""

    def __init__(self, *args, **kwargs):
        systemid = kwargs.pop('systemid')
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['leader'] = forms.ModelChoiceField(
                required=False,
                queryset=Member.objects.all(),
                widget=forms.Select(attrs={'title': _("Add leader")})
            )
    class Meta:
        model = Organization
        exclude = ('leader',)

class ActionGroupForm(ModelForm):
    class Meta:
        model = ActionGroup
        """
    leader = forms.ModelChoiceField(queryset=Member.objects.all())
    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['leader'] = [t.pk for t in
                    kwargs['instance'].leader_set.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)
    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m
        def save_m2m():
            old_save_m2m()
            instance.leader_set.clear()
            for leader in self.cleaned_data['leader']:
                instance.leader_set.add(leader)
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()
        return instance
        """


class GrantForm(ModelForm):
    class Meta:
        model = Grant
        exclude = ('date_applied','approval_status',)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('approval_status','date_applied','progress_status',)

