from django.db import models
from django.utils.translation import ugettext_lazy as _

#from profiles.models import Profile
from django.db import models

# Workflow models

class Project(models.Model):
    title = models.CharField(_("title"), max_length=50, null=True, blank=True)


