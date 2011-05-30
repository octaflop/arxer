from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, UserManager, Permission
##from idios.models import ProfileBase
from photologue.models import Gallery, Photo, ImageModel
from pinax.apps.profiles.models import Profile
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify

from verbena.managers import ProjectManager

from django.utils.translation import ugettext_lazy as _

##from pinax.apps.profiles.models import Profile
##from pinax.apps.tribes.models import Tribe
from settings import STATIC_ROOT, MEDIA_ROOT

import datetime

#############################################################################
# INDIVIDUAL-based models
# Organization -> a non-individual user
# Action individual, Student, Faculty (admin is untouched?) -> individual users

class Member(models.Model):
    """ An abstract to represent all signed-in users"""
    profile = models.ForeignKey(User, blank=True, related_name='member_profile')
    slug = models.SlugField(_("URL-friendly name"), max_length=80)#, unique=True)
    avatar = models.ForeignKey(Photo, related_name='member_avatar', blank=True)

    objects = UserManager()

    def __unicode__(self):
        return self.profile.username

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def is_student(self):
        try:
            if self.pk == self.student.pk:
                return True
            else:
                return False
        except:
            return

    def is_faculty(self):
        try:
            if self.pk == self.faculty.pk:
                return True
            else:
                return False
        except:
            return

    # Will be overridden by student & faculty views (I hope)
    @models.permalink
    def get_absolute_url(self):
        return ('member_view', [str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.profile.username)
            super(Member, self).save(*args, **kwargs)

class GeneralMember(Member):
    """ An entity representing a registered, unaffiliated user.
        Individual persons are represented in this way. This ensures that only
        individuals can sign up for projects and volunteer events.
        This is also the main model for initial signups.
        * apply for grants
    """
    how_heard = models.TextField(_("Reference"),
            help_text=_("How did you hear about us?"),
            blank=True)

    class Meta:
        verbose_name = _("General Member")

class Organization(Member):
    """ Organizations are entities applying for projects or grants.
    Organizations share a single login.
    Organizations may not apply for workshops and participate in volunteer
    events.
    CHANGED AGAIN = Organizations are now sub-classes of Members (again)
    """
    title = models.CharField(_("Organization name"),
            help_text=_("The name of your organization"),
            max_length=100,
            unique=True)
    org_slug = models.SlugField(_("URL-friendly name for organization"))
    community = models.CharField(
            _("What community do you represent or work with?"),
            max_length=180,
            blank=True)
    mandate = models.CharField(
            _("What is your organization's goal or mandate?"),
            max_length=180,
            blank=True)
    service = models.TextField(
            _("How does your organization goal or mandate fit in with our\
                desire to support community organizations?"),
            blank=True)
    funding = models.TextField(
            _("What are your organization's principal sources of funding?"),
            blank=True)
    annual_budget = models.CharField(
            _("What is your organization's annual budget?"),
            max_length=25,
            blank=True)
    nonprofit_status = models.BooleanField(
            _("Are you a registered non-profit?"),
            default=False)
    about = models.TextField(_("About"))
    location = models.ForeignKey("Location", blank=True)
    website = models.URLField(_("website"), blank=True, null=True)

    @property
    def leader(self):
        return self.profile

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
    
    @models.permalink
    def get_absolute_url(self):
        return ('org_view', [str(self.org_slug)])

# Call time options for students and faculty
CALL_TIMES = (
            ('MO', 'Morning'),
            ('AF', 'Afternoon'),
            ('EV', 'Evening'),
        )

class Student(GeneralMember):
    """
        A student must be able to:
        * apply for an ARX project
        * Request to book a room
        * Lookup volunteer opportunities
        * Choose to receive the newsletter
    """
    phone = PhoneNumberField(_("Phone Number"), blank=True, null=True)
    call_time = models.CharField(_("Best time to call"),
            help_text=_("Generally, when is the best time to call?"),
            choices=CALL_TIMES,
            max_length=2,
            blank=True, null=True)
    studying = models.CharField(_("Course of study"), max_length=80,
            blank=True, null=True)
    comp_year = models.IntegerField(_("Expected year of completion"),
            max_length=4,
            blank=True, null=True)

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    @models.permalink
    def get_absolute_url(self):
        return ('student_view', [str(self.slug)])

class Faculty(GeneralMember):
    """
    * Book a presentation
    * Choose to receive the newsletter
    They may not apply for grants
    """
    # The faculty the faculty member is in 
    in_faculty = models.CharField(_("Is a member of faculty"),
            max_length=80, blank=True, null=True)
    phone = PhoneNumberField(_("Phone Number"), blank=True, null=True)
    phone_ext = models.CharField(_("Phone extension"),
            blank=True,
            max_length=10, null=True)
    call_time = models.CharField(_("Best time to call"),
            help_text=_("Generally, when is the best time to call?"),
            choices=CALL_TIMES,
            max_length=2, blank=True, null=True)
    class Meta:
        verbose_name = _("faculty member")
        verbose_name_plural = _("faculty members")

    @models.permalink
    def get_absolute_url(self):
        return ('faculty_view', [str(self.slug)])

#############################################################################
# GROUP-Based Models
# Each of these models refers to individuals in some way.
class ActionGroup(models.Model):
    """ Action groups are groups led by a leader to accomplish a goal.
    Action groups may be supported by any member, but only led & started by
    GeneralMembers """
    title = models.CharField(_("Action Group title"), max_length=80)
    slug = models.SlugField(_("URL-friendly title"))
    portrait = models.ForeignKey(Photo, related_name='actiongroup_portrait',
            null=True, blank=True)
    leader = models.ForeignKey("GeneralMember", related_name='ag_leader')
    # a required portrait
    # Similar to facebook's "like"
    supporters = models.ManyToManyField(GeneralMember,
            related_name = "group-supporters",
            blank=True)
    photos = models.ManyToManyField(Gallery,
            related_name = "group-photos",
            blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Action group")
        verbose_name_plural = _("Action groups")

    @models.permalink
    def get_absolute_url(self):
        return ('act_view', [str(self.slug)])

class Research(models.Model):
    """ Research & Resources have their own logos and pages """
    title = models.CharField(_("Group title"), max_length=80)
    slug = models.SlugField(_("URL-friendly title"))
    portrait = models.ForeignKey(Photo, related_name='research_portrait',
            null=True, blank=True)
    supporters = models.ManyToManyField(Member,
            related_name = "research-supporters",
            blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('res_view', [str(self.slug)])

class Location(models.Model):
    """
    A Location is simply a latitude and longitude
    """
    ## Default data == Woodwards @ Vancouver
    latitude = models.FloatField(blank=True, default=49.28227)
    longitude = models.FloatField(blank=True, default=-123.10754)
    place = models.CharField(_("The name of the location"), max_length=100,\
            default=_("Vancouver"))

    def __unicode__(self):
        return self.place

class Event(models.Model):
    """
    ABSTRACT Model
    Events are anything occurring at a specific time
    """
    title = models.CharField(_("Event title"), max_length=100)
    slug = models.SlugField(
        _("URL-friendly name"),
        help_text=_("A URL-Friendly title for your event")
    )
    start_date = models.DateTimeField(_("Event start date & time"))
    end_date = models.DateTimeField(_("Event end date & time"))
    location = models.ForeignKey(Location, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-start_date',)

    @models.permalink
    def get_absolute_url(self):
        return ('event_view', [str(self.slug)])

class Workshop(Event):
    """
    A workshop is an event with members
    Workshops are held by SFPIRG at the request of a user
    """
    room = models.CharField(_("Room"), max_length=80, blank=True)
    # organizations may NOT sign up for a workshop
    members = models.ManyToManyField(GeneralMember,
            related_name = "workshops",
            verbose_name = "members",
        )

    @models.permalink
    def get_absolute_url(self):
        return ('workshop_view', [str(self.slug)])

class VolunteerOpportunity(Event):
    """
    A volunteer opportunity is an event with an organization and members
    organization may NOT sign up (GeneralMembers only)
    """
    organization = models.ForeignKey(Organization)
    volunteers = models.ManyToManyField(GeneralMember,
            related_name = "volunteer-opportunities",
            verbose_name = "volunteers",
        )
    class Meta:
        verbose_name = _("volunteer opportunity")
        verbose_name_plural = _("volunteer opportunities")

    @models.permalink
    def get_absolute_url(self):
        return ('volunteer_view', [str(self.slug)])

# Project types
PROJECT_TYPE = (
    (_("CO"), _("Computer Related")),
    (_("CR"), _("Creative")),
    (_("FR"), _("Formal Research")),
    (_("OD"), _("Organizational Development")),
    (_("SU"), _("Survey")),
    (_("OT"), _("Other")),
)

# Possible Project statuses
PROJECT_APPROVAL_STATUS = (
    (_("PR"), _("Proposed")),
    (_("RE"), _("Received")),
    (_("PE"), _("Pending")),
    (_("DN"), _("Denied")),
    (_("AP"), _("Approved")),
)

PROJECT_PROGRESS_STATUS = (
    (_("PO"), _("Populating")),
    (_("PL"), _("Planning")),
    (_("IP"), _("In Progress")),
    (_("FS"), _("Finished - Successful")),
    (_("FU"), _("Finished - Unsuccessful")),
)

# Project-Based Models

#ARX Projects: The moneymaker
class Project(models.Model):
    """
    Projects are the ARX projects.
    Only organizations can create projects.
    """
    title = models.CharField(_("Project title"),
            help_text=_("Project title (be clear and short)"),
            max_length=80)
    slug = models.SlugField(_("URL-friendly name"))
    portrait = models.ForeignKey(Photo, related_name='project_portrait',
            null=True, blank=True)
    date_applied = models.DateField(_("Project start date"))
    research_question = models.TextField(_("Central Research Question"),
            help_text=_("What is the central research question you want answered?"),
            blank=True
            )
    type_comp_rel = models.BooleanField(_("Computer related"),
            help_text=_("These boxes indicate your project type.\
                        Please select all that apply."),
            blank=True)
    type_creative = models.BooleanField(_("Creative"),
            help_text=_("These boxes indicate your project type.\
                        Please select all that apply."),
            blank=True)
    type_form_res = models.BooleanField(_("Formal Research"),
            help_text=_("These boxes indicate your project type.\
                        Please select all that apply."),
            blank=True)
    type_org_dev = models.BooleanField(_("Organizational Development"),
            help_text=_("These boxes indicate your project type.\
                        Please select all that apply."),
            blank=True)
    type_survey = models.BooleanField(_("Survey"),
            help_text=_("These boxes indicate your project type.\
                        Please select all that apply."),
            blank=True)
    type_other = models.BooleanField(_("Other (please indicate)"),
            help_text=_("These boxes indicate your project type.\
                        Please select all that apply."),
            blank=True)
    other_project_type = models.CharField(_("Other description"),
            help_text=_("If you checked 'other,' please briefly \
                        describe your project-type."),
            max_length=200,
            blank=True)
    magnitude = models.TextField(_("Scope of Project"),
            help_text=_("Describe the size of the project in quantifiable terms\
                (e.g. word/page count, duration of radio, number of hours)."),
            )
    project_description = models.TextField(_("Project Description"),
            help_text=_("Please describe your project here")
            )
    issues = models.TextField(_("Issues Address"),
            help_text=_("What social/environmental issues are addressed by this project?")
            )
    results_plan = models.TextField(_("Resultant goal"),
            help_text=_("How do you plan on using the results of this project?")
            )
    goal = models.TextField(_("Project goal"),
            help_text=_("What larger goal is served by undertaking this project?")
            )
    approval_status = models.CharField(_("approval status"),
            max_length=2, choices=PROJECT_APPROVAL_STATUS,
            default="PR",
            blank=False)
    progress_status = models.CharField(_("progress status"),
            max_length=2, choices=PROJECT_PROGRESS_STATUS,
            default="PO",
            blank=False)
    # manager:
    approved = ProjectManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('project_view', [str(self.slug)])

    def save(self, *args, **kwargs):
        self.date_applied = datetime.datetime.now()
        super(Project, self).save(*args, **kwargs)

class StudentProject(Project):
    """
    Only student can sign up for these projects.
    """
    student_leader = models.ForeignKey(Student)
    professor = models.ForeignKey(Faculty, blank=True)
    course_name = models.CharField(_("Course name"),
            help_text=_("Course name and number"),
            max_length=100,
            blank=True)
    course_apply = models.TextField(_("Course application"),
            help_text=_("How would you like to apply this project in your\
                course?"),
            blank=True)

# Grant Progress
GRANT_STATUS = (
    (_("SU"), _("Submitted")),
    (_("PE"), _("Pending")),
    (_("AP"), _("Approved")),
    (_("DN"), _("Denied")),
)

# Grant Type (amount)
GRANT_TYPE = (
    (_("SM"), _("Small")),
    (_("LA"), _("Large")),
)


class Grant(models.Model):
    """
    A grant application model, written to spec of client.
    """
    grant_type =  models.CharField(_("Grant type"), max_length=2,
            choices=GRANT_TYPE,
            help_text="Small: up to $500. Large: $500-$1000")
    title = models.CharField(_("Grant title"),
            help_text="The title of the grant-request",
            max_length=100)
    slug = models.SlugField(_("Slug"),
            help_text="The slug is the URL-friendly title")
    date_applied = models.DateTimeField(_("Date Applied"))
    org_name = models.ForeignKey(Organization)
    applicant_name = models.CharField(_("Applicant's Name"), max_length=100)
    mail_address = models.TextField(_("Mailing address with postal code"))
    email = models.EmailField(_("Contact email"))
    phone = PhoneNumberField(_("Phone Number"))
    approval_status = models.CharField(_("approval status"),
            max_length=2, choices=PROJECT_APPROVAL_STATUS,
            default="PR",
            blank=False)
    accessibility_opt = models.BooleanField(_("Accessibility Grant"),
            help_text=("Select this option if you are applying for an\
            accessibility grant in conjunction with your request."))
    other_fund = models.TextField(_("Other funding sources"),
            help_text="Where else have you applied for funding?",
            blank=True)
    description = models.TextField(_("Project description"),
            help_text="What are you requesting this money for? Please briefly\
            describe your project/campaign/event.")
    comm_benefit = models.TextField(_("Community Benefit"),
        help_text="How does this initiative benefit the community?")
    budget_timeline = models.TextField(_("Breakdown and Timeline"),
            help_text="Please provide a project break-down and timeline")
    mandate = models.TextField(_("Mandate"), help_text="What is the mandate of\
            your organization?")
    history = models.TextField(_("History"),
        help_text="How long has your project been around and what are some of\
        your past projects/initiatives?")
    magnitude = models.TextField(_("Amount of people"),
            help_text="How may people are working on this project and how does\
            your organization make decisions?")
    how_heard = models.TextField(_("Reference"),
            help_text="How did you hear about SFPIRG action grants?")

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('grant_view', [str(self.slug)])

    def save(self, *args, **kwargs):
        self.date_applied = datetime.datetime.now()
        super(Grant, self).save(*args, **kwargs)

################################################################################
# Flatpage entities
# These models can be edited, but do not contain "members"

class NewsRelease(models.Model):
    """
    A News release is a short document with up-to-date information for the
    press and other public media entities.
    """
    content = models.TextField(_("A description of the news"))
    datetime_released = models.DateTimeField(_("News Release date and time"),
            help_text=_("Indicate the date and time of the news release"))

class Navigation(models.Model):
    """
    A model referring back to the site structure to build links based on images
    """
    title = models.CharField(_("Menu title"), max_length=80)
    link = models.CharField(_("URL reference"), max_length=80)
    menu_slug = models.SlugField(_("Menu slug"), help_text=_("A\
            template-friendly name, such as 'action-group'"))
    navlogo_path = models.FilePathField(_("Logo path"), help_text=_("Path to\
            navigation logo, based on STATIC_URL, include name. Must be a\
            png."), path="%s/%s" % (STATIC_ROOT, "nav"), blank=True, recursive=True)
    weight = models.IntegerField(default=0)

    class Meta:
        ordering = ["weight"]
        verbose_name_plural = "Navigation Paths"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.navlogo_path = str(self.navlogo_path).replace(STATIC_ROOT, '')
        self.navlogo_path = "%s%s" % ("/site_media/static", self.navlogo_path)
        super(Navigation, self).save(*args, **kwargs)

################################################################################
# Listeners
################################################################################
def create_member(sender, **kwargs):
    """
    Create a new member when a User object is saved
    """
    # Check for a new user
    if not kwargs['created']:
        return

    # get the User account instance
    user = kwargs['instance']

    # don't make a member if it already exists
    try:
        p = Member.objects.get(profile=user)
        return p
    except Member.DoesNotExist:
        p = None
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(
            user = user,
        )
        profile.save()
    member = GeneralMember(
        profile = user,
    )
    member.save()

post_save.connect(create_member, sender=User)


def grant_addgroup_perms(sender, **kwargs):
    """
    Grant permission to faculty and students to create groups
    """
    user = kwargs['instance']
    perms = Permission.objects.get(codename='add_actiongroup')
    user.profile.user_permissions.add(perm)
    user.save()
    return user

post_save.connect(grant_addgroup_perms, sender=Student)
post_save.connect(grant_addgroup_perms, sender=Faculty)

def grant_arx_perms(sender, **kwargs):
    """
    Grant permission to organizations to manage arx:
        - add new project
        - delete their own project
    """
    user = kwargs['instance']
    perms = Permission.objects.get(codename='add_project')
    user.profile.user_permissions.add(perms)
    user.save()
    return user

post_save.connect(grant_arx_perms, sender=Organization)
