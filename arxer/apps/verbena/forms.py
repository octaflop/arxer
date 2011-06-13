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
from django.utils.translation import ugettext
from ajax_select.fields import AutoCompleteSelectField
from pinax.apps.account.utils import perform_login
from tinymce.widgets import TinyMCE

from verbena.recaptchawidget.fields import ReCaptchaField
import re
alnum_re = re.compile(r"^\w+$")

class GroupForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop("group", None)
        super(GroupForm, self).__init__(*args, **kwargs)


class LoginForm(GroupForm):
    
    password = forms.CharField(
        label = _("Password"),
        widget = forms.PasswordInput(render_value=False)
    )
    
    user = None
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        ordering = []
        self.fields["username"] = forms.CharField(
            label = ugettext("Username"),
            max_length = 30,
        )
        ordering.append("username")
        ordering.extend(["password",])
        self.fields.keyOrder = ordering
    
    def user_credentials(self):
        """
        Provides the credentials required to authenticate the user for
        login.
        """
        credentials = {}
        credentials["username"] = self.cleaned_data["username"]
        credentials["password"] = self.cleaned_data["password"]
        return credentials
    
    def clean(self):
        if self._errors:
            return
        user = authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is currently inactive."))
        else:
            error = _("The username and/or password you specified are not correct.")
            raise forms.ValidationError(error)
        return self.cleaned_data
    
    def login(self, request):
        perform_login(request, self.user)
        request.session.set_expiry(60 * 60 * 24 * 7 * 3)



class AvatarForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ('effect', 'tags', 'effect', 'crop_from', 'is_public',)

class ProjectForm(ModelForm):
    class Meta:
        #model = StudentProject
        model = Project
        exclude = ('approval_status','date_applied','progress_status','portrait','student_leader','professor','organization',)

class EventForm(ModelForm):
    class Meta:
        model = Event

class LocationForm(ModelForm):
    class Meta:
        model = Location

class UserForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(),
            label=_("Please confirm your password"))
    email = forms.EmailField()
    recaptcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ugettext("E-mail (optional)")
        self.fields["email"].required = False

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        return value

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data

    def create_user(self, username=None, commit=True):
        user = User()
        if username is None:
            raise NotImplementedError("UserForm.create_user does not handle "
                "username=None case. You must override this method.")
        user.username = username
        user.email = self.cleaned_data["email"].strip().lower()
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    def login(self, request, user):
        # nasty hack to get get_user to work in Django
        user.backend = "django.contrib.auth.backends.ModelBackend"
        perform_login(request, user)

    def save(self, request=None):
        # don't assume a username is available. it is a common removal if
        # site developer wants to use e-mail authentication.
        username = self.clean_username()
        email = self.clean_email()
        if self.is_valid():
            new_user = self.create_user(username)
            return new_user
        else:
            return


class MemberForm(ModelForm):
    class Meta:
        model = Member

class MemberForm(ModelForm):
    class Meta:
        model = Member

class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        exclude = ('member',)

class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ('member',)

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
        exclude = ('location','leader','approval_status',)
        fields = ('title', 'org_slug', 'about', 'mandate',
                'community','service', 'funding', 'annual_budget',
                'nonprofit_status', 'website',)

class ActionGroupForm(ModelForm):
    about = forms.CharField(widget=TinyMCE(attrs={'cols':80, 'rows':30}))
    class Meta:
        model = ActionGroup
        fields =('title', 'slug','about',)
        exclude = ('supporters','gallery',)

class GrantForm(ModelForm):
    class Meta:
        model = Grant
        exclude = ('date_applied','approval_status','applicant',)

