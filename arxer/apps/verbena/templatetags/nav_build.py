from django import template
from verbena.models import Navigation
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('verbena/templatetags/sfpirgnav.html', takes_context=True)
def sfpirgnav(context):
    navi = Navigation.objects.all()
    context['navi'] = navi
    return dict(navi=context['navi'])

@register.inclusion_tag('verbena/templatetags/sfpirgnavsub.html')
def sfpirgnavsub(menu):
    navi = Navigation.objects.get_or_create(menu_slug=menu)
    if navi[1]:
        navi = navi[0]
    else:
        navi.title = "%s" % (menu)
        navi.link = "#"
        navi.navlogo_path = "/site_media/static/nav/%s-nav-icon.png" % (menu)
    return dict(navi=navi)

@register.inclusion_tag('verbena/templatetags/search.html', takes_context=True)
def searchbox(context):
    search = {
            'prompt': _("search"),
            }
    context['searchbox'] = search
    return dict(searchbox=context['searchbox'])
