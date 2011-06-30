from django.db import models

class SlideManager(models.Manager):
    """
    Returns published slides
    """
    def get_query_set(self):
        return super(SlideManager, self).get_query_set().filter(is_published=True)

