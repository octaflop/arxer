from verbena.models import Organization, Grant, Project, ActionGroup, Member
from django.forms import ModelForm
import django.forms as forms
from django.template.defaultfilters import slugify

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization

class ActionGroupForm(ModelForm):
    class Meta:
        model = ActionGroup
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


class GrantForm(ModelForm):
    class Meta:
        model = Grant
        exclude = ('date_applied','approval_status',)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('approval_status','date_applied','progress_status',)

