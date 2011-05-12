from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Event
from verbena.forms import EventForm

event_list = {
    "queryset" : Event.objects.all(),
}

event_add = {
    "model" : Event,
    "login_required" : True,
}

event_edit = {
    "form_class" : EventForm,
    "login_required" : True,
}

urlpatterns = patterns("",
    url(r"^$", object_list, event_list, name="event_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, event_list, name="event_view"),
    url(r"^add/$", create_object, event_add, name="event_add"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, event_edit,
        name="event_edit"),
)

