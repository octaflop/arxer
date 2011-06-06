from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Workshop
from verbena.forms import WorkshopForm

workshop_list = {
    "queryset" : Workshop.objects.all(),
    "template_name": "verbena/events/event_list.html",
}

workshop_add = {
    "model" : Workshop,
    "login_required" : True,
    "template_name": "verbena/events/event_form.html",
}

workshop_edit = {
    "form_class" : WorkshopForm,
    "login_required" : True,
    "template_name": "verbena/events/event_form.html",
}

urlpatterns = patterns("",
    url(r"^$", object_list, workshop_list, name="workshop_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, workshop_list, name="workshop_view"),
    url(r"^add/$", create_object, workshop_add, name="workshop_add"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, workshop_edit,
        name="workshop_edit"),
)

