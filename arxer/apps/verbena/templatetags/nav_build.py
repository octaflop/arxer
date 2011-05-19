from django import template
from verbena.models import Navigation, SubNavigation
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('verbena/templatetags/sfpirgnav.html', takes_context=True)
def sfpirgnav(context):
    navi = Navigation.objects.all()
    context['navi'] = navi
    return dict(navi=context['navi'])

@register.inclusion_tag('verbena/templatetags/sfpirgnavsub.html', takes_context=True)
def sfpirgnavsub(context, menu):
    navi = SubNavigation.objects.all()
    navi = navi.filter(nav_key__menu_slug=menu)
    if navi.exists():
        context['navi'] = navi
    else:
        context['navi'] = None
    return dict(navi=context['navi'])

@register.inclusion_tag('verbena/templatetags/search.html', takes_context=True)
def searchbox(context):
    search = {
            'prompt': _("search"),
            }
    context['searchbox'] = search
    return dict(searchbox=context['searchbox'])
