from django.db import models
from django.utils.translation import ugettext_lazy as _

# import pinax profile
from pinax.apps.profiles.models import Profile
#from profiles.models import Profile
from django.db import models

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

# Workflow models

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
    faculty = models.CharField(_("Is a member of faculty"), max_length=80)

    class Meta:
        verbose_name = _("faculty member")
        verbose_name_plural = _("faculty members")

#class Page(models.Model):
#    """ The page abstract model """
#    title = models.CharField(_("title"), max_length=50, null=True, blank=True)
#
#    def __unicode__(self):
#        return self.title

class Page(models.Group):


class Organization(Page):
    """ An organization must be approved by an SFPIRG admin """
    admin = models.ForeignKey(Profile, related_name="administrator")
    members = models.ManyToManyField(Profile)#, related_name="members")

class ActionGroup(Page):
    """
        The Action Group model:
        An action group is an ad-hoc page affiliated with SFPIRG
        each page is adjustable by the user
        An action group user must be able to:
        * email the action-group supporter
        * update content on their specific page

    """
    group_name = models.CharField(_("group name"), max_length=50)

class Project(ActionGroup):
    """
        The model for projects
        In addition to the communication aspects of an action-group, projects
        can also recruit new members and have a listed location.
        They also have organizations backing them up, which also means that
        their statuses are closely followed.
    """
    location = models.CharField(_("location"), max_length=150, null=True, blank=True)
    organization = models.ForeignKey(Organization)
    approval_status = models.CharField(_("approval status"), max_length=2, choices=PROJECT_APPROVAL_STATUS)
    progress_status = models.CharField(_("progress status"), max_length=2, choices=PROJECT_PROGRESS_STATUS)

    def __unicode__(self):
        return self.title

