from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_noop as _
from django.db.models.signals import post_syncdb

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        # admin notifications
        notification.create_notice_type("new_org", _("New Organization Created"),
                _("Someone has created a new organization"))
        notification.create_notice_type("new_arx",
                _("New Action Research Project"),
                _("Someone has created a new action research project"))
        notification.create_notice_type("new_grant",
                _("New Grant"),
                _("Someone has applied for a new grant"))
        # arx/org notifications
        notification.create_notice_type("arx_approved", _("ARX Approved"),
                _("The admins have approved the ARX"))
        notification.create_notice_type("arx_denied", _("ARX Denied"),
                _("The admins have denied the ARX"))
        notification.create_notice_type("org_approved", _("Organization Approved"),
                _("The admins have approved the new organization"))
        notification.create_notice_type("org_denied", _("Organization Denied"),
                _("The admins have denied the new organization"))
        notification.create_notice_type("grant_approved", _("Grant Approved"),
                _("The admins have approved the new grant"))
        notification.create_notice_type("grant_denied", _("Grant Denied"),
                _("The admins have denied the new grant"))
    post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping notification creation as notification app has not been found"

class ProjectManager(models.Manager):
    """
    Returns approved projects
    """
    def get_query_set(self):
        return super(ProjectManager, self).get_query_set().filter(approval_status="AP")


