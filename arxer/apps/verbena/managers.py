from django.db import models

class ProjectManager(models.Manager):
    """
    Returns approved projects
    """
    def get_query_set(self):
        return super(ProjectManager, self).get_query_set().filter(approval_status="AP")
