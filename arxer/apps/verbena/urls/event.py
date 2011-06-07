from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Event
from verbena.forms import EventForm
from verbena.views import ev_list
import datetime

event_list = {
    "queryset" : Event.objects.filter(end_date__gte=datetime.datetime.now()),
    "template_name" : "verbena/events/event_list.html",
}

event_add = {
    "model" : Event,
    "login_required" : True,
    "template_name" : "verbena/events/event_form.html",
}

event_edit = {
    "form_class" : EventForm,
    "login_required" : True,
    "template_name" : "verbena/events/event_form.html",
}

event_detail = {
    "queryset" : Event.objects.all(),
    "template_name" : "verbena/events/event_detail.html",
}

urlpatterns = patterns("",
    #url(r"^$", object_list, event_list, name="event_home"),
    url(r"^$", ev_list, event_list, name="event_home"),
    url(r"^add/$", create_object, event_add, name="event_add"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, event_detail, name="event_view"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, event_edit,
        name="event_edit"),
)

