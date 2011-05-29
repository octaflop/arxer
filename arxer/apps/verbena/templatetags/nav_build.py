from django import template
from verbena.models import Navigation##, SubNavigation
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('verbena/templatetags/sfpirgnav.html', takes_context=True)
def sfpirgnav(context):
    navi = Navigation.objects.all()
    context['navi'] = navi
    return dict(navi=context['navi'])

#@register.inclusion_tag('verbena/templatetags/sfpirgnavsub.html')#, takes_context=True)
#def sfpirgnavsub(menu):
#    ##context['navi'] = SubNavigation.objects.filter(nav_key__menu_slug=menu)
#    navi = SubNavigation.objects.filter(nav_key__menu_slug=menu)
#    return dict(navi=navi)

@register.inclusion_tag('verbena/templatetags/search.html', takes_context=True)
def searchbox(context):
    search = {
            'prompt': _("search"),
            }
    context['searchbox'] = search
    return dict(searchbox=context['searchbox'])

@register.inclusion_tag('verbena/templatetags/memberbox.html', takes_context=True)
def memberbox(context):
    if 'user' in context:
        user = context['user']
        usm = User.objects.get(username=user.username)
        member = usm.member_profile.get()
    else:
        user = None
        member = None
    return dict(user=user, member=member)
