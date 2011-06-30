from django.db import models
from django.utils.translation import ugettext_lazy as _
from managers import SlideManager

# Create your models here.
IMAGE_DIMS = u"800x600"

class Slide(models.Model):
    """
    An abstract slide class for use by the templatetag
    """
    title = models.CharField(_("Slide title"), max_length=100)
    slug = models.SlugField(_("URL-friendly name"), max_length=80, unique=True)
    image = models.ImageField(_("Image"), upload_to='slide_image',
            help_text=_("The slide image. This will be resized, so use the\
                    dimensions: %s if you don't want any issues" % IMAGE_DIMS))
    description = models.TextField(_("Description"), max_length=500,
            help_text=_("A short description under the title. You may add\
                links by using the markdown syntax"))
    is_published = models.BooleanField(_("Published?"), help_text=_("Only\
            published slides are shown"))
    link = models.URLField(_("Slide Link"))
    weight = models.IntegerField(_("Weight"), default=0, help_text=_("Weights\
        determine slide-ordering. Lower weights are higher on the page"))

    # manager
    published = SlideManager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")

"""
An example of extension. This will be moved to the app in a later iteration
TODO
"""
class FrontPageSlide(Slide):
    pass

class ARXSlide(Slide):
    pass
