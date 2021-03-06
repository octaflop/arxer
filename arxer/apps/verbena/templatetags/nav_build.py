from django import template
from verbena.models import Navigation, Event
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime
from verbena.models import Chunk
from verbena.forms import LoginForm

register = template.Library()

# CHUNK Tags
@register.inclusion_tag('verbena/templatetags/chunk.html', takes_context=True)
def chunk(context, slug):
    """
    Inserts the contents of a flatpage by looking up the chunk slug
    eg:
        {% chunk "actiongroup" %}
    """
    try:
        context['chunk'] = Chunk.objects.get(slug=slug)
    except Chunk.DoesNotExist:
        context['chunk'] = ''
    return dict(chunk=context['chunk'])

@register.inclusion_tag('verbena/templatetags/colchunk.html', takes_context=True)
def colchunk(context, slug):
    """
    Inserts the contents of a flatpage by looking up the chunk slug. This chunk
    is a column.
    eg:
        {% colchunk "actiongroup" %}
    """
    try:
        context['chunk'] = Chunk.objects.get(slug=slug)
    except Chunk.DoesNotExist:
        context['chunk'] = ''
    return dict(chunk=context['chunk'])

@register.inclusion_tag('verbena/templatetags/imgchunk.html', takes_context=True)
def imgchunk(context, slug):
    """
    Inserts the contents of a flatpage by looking up the chunk slug. This chunk
    is a column.
    eg:
        {% imgchunk "actiongroup" %}
    """
    try:
        context['chunk'] = Chunk.objects.get(slug=slug)
    except Chunk.DoesNotExist:
        context['chunk'] = ''
    return dict(chunk=context['chunk'])

# Site-Wide tags
# dynamic tags
@register.inclusion_tag('verbena/templatetags/newsbox.html', takes_context=True)
def newsbox(context):
    events = Event.objects.filter(end_date__gte=datetime.datetime.now())
    context['news'] = events
    return dict(news=context['news'])

@register.inclusion_tag('verbena/templatetags/sfpirgnav.html', takes_context=True)
def sfpirgnav(context):
    navi = Navigation.objects.all()
    context['navi'] = navi
    return dict(navi=context['navi'])

@register.inclusion_tag('verbena/templatetags/search.html', takes_context=True)
def searchbox(context):
    search = {
            'prompt': _("search"),
            }
    context['searchbox'] = search
    return dict(searchbox=context['searchbox'])

@register.inclusion_tag('verbena/templatetags/loginbox.html', takes_context=True)
def loginbox(context):
    loginform = LoginForm()
    return dict(form=loginform)

@register.inclusion_tag('verbena/templatetags/memberbox.html', takes_context=True)
def memberbox(context):
    if 'user' in context:
        user = context['user']
        usm = User.objects.filter(username=user.username)[0]
        member = usm.member
    else:
        user = None
        member = None
    return dict(user=user, member=member)
