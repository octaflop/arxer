from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from pinax.apps.profiles.models import Profile
from pinax.apps.tribes.models import Tribe

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


# Profile-based models
# Action individual, Organization, Student, Faculty (admin is untouched?)
class ActionIndividual(Profile):
    """ Action individuals are leaders of action-groups """
    pass

class Organization(models.Model):
    """ Organizations are entities applying for projects or grants.
    Organizations share a single login """
    name = models.CharField(_("Name"), max_length=80)
    slug = models.SlugField(_("Slug"), max_length=80)
    about = models.TextField(_("About"))
    location = models.ForeignKey("Location")
    website = models.URLField(_("website"), blank=True, null=True)
    workshops = models.ForeignKey("Workshop", blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('org_view', [str(self.slug)])

class Student(Profile):
    """
        A student must be able to:
        * apply for an ARX project
        * apply for grants
        * Request to book a room
        * Lookup volunteer opportunities
        * Choose to receive the newsletter
    """
    studying = models.CharField(_("Course of study"), max_length=80)
    comp_year = models.IntegerField(_("Expected year of completion"),
            max_length=4)

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

class Faculty(Profile):
    """
    * Book a presentation
    * Choose to receive the newsletter
    """
    # The faculty the faculty member is in 
    in_faculty = models.CharField(_("Is a member of faculty"),
            max_length=80)

    class Meta:
        verbose_name = _("faculty member")
        verbose_name_plural = _("faculty members")

# Page-Based Models
class ActionGroup(Tribe):
    """ Action groups are groups led by a leader to accomplish a goal """
    title = models.CharField(_("Action Group title"), max_length=80)
    leader = models.ForeignKey("ActionIndividual")

class NewsRelease(models.Model):
    """
    A News release is a short document with up-to-date information for the
    press and other public media entities.
    """
    content = models.TextField(_("A description of the news"))
    datetime = models.DateTimeField()

class Location(models.Model):
    """
    A Location is simply a latitude and longitude
    """
    latitude = models.FloatField(blank=True, default=49.28227)
    longitude = models.FloatField(blank=True, default=-123.10754)
    place = models.CharField(_("The name of the location"), max_length=100,\
            default=_("Vancouver"))

    def __unicode__(self):
        return self.place

class Event(models.Model):
    """
    Events are anything occurring at a specific time
    """
    title = models.CharField(_("Event title"), max_length=100)
    slug = models.SlugField(_("Event slug"))
    start_date = models.DateTimeField(_("Workshop start date & time"))
    end_date = models.DateTimeField(_("Workshop end date & time"))
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-start_date',)
        get_latest_by = 'start_date'

class Workshop(Event):
    """
    A workshop is an event with members
    """
    room = models.CharField(_("Room"), max_length=80, blank=True)
    members = models.ManyToManyField(User,
            related_name = "workshops",
            verbose_name = "members",
            )

class Gathering(Event):
    """
    A gathering is an open event
    """
    pass

class VolunteerOpportunity(Event):
    """
    A volunteer opportunity is an event with an organization and members
    """
    organization = models.ForeignKey(Organization)
    volunteers = models.ManyToManyField(User,
        related_name = "volunteer opportunities",
        verbose_name = "volunteers",
    )
    class Meta:
        verbose_name = _("volunteer opportunity")
        verbose_name_plural = _("volunteer opportunities")

# Project-Based Models
class Project(Tribe):
    title = models.CharField(_("Project title"), max_length=80)
    approval_status = models.CharField(_("approval status"),\
            max_length=2, choices=PROJECT_APPROVAL_STATUS, blank=False)
    progress_status = models.CharField(_("progress status"),\
            max_length=2, choices=PROJECT_PROGRESS_STATUS, blank=False)

    def __unicode__(self):
        return self.title

class ProjectMember(models.Model):
    """
    A simple abstract for linking users to projects
    """
    project = models.ManyToManyField(Project,\
            related_name="%(app_label)s_%(class)s_related")
    user = models.ForeignKey(User)
