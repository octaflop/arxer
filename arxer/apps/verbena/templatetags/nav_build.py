from django import template
from verbena.models import Navigation

register = template.Library()

#@register.inclusion_tag('verbena/sfpirgnav.html', takes_context=True)
def sfpirgnav(context):
    navi = Navigation.objects.all()
    context['navi'] = navi
    return dict(navi=context['navi'])

register.inclusion_tag('verbena/templatetags/sfpirgnav.html', takes_context=True)(sfpirgnav)

def sfpirgnavsub(context, menu=None):
    if menu:
        navi = Navigation.objects.get(menu_slug=menu)
    else:
        navi = Navigation.objects.all()
    context['navi'] = navi
    return dict(navi=context['navi'])

register.inclusion_tag('verbena/templatetags/sfpirgnavsub.html', takes_context=True)(sfpirgnav)

def sfpirgnavsubsub():
    return None
