from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Grant
from verbena.forms import GrantForm
from verbena.views import add_grant

grant_list = {
    "queryset" : Grant.objects.all(),
    "template_name" : "verbena/grants/grant_list.html",
}

grant_add = {
    #"model" : Grant,
    "form_class" : GrantForm,
    "template_name" : "verbena/grants/grant_form.html",
}

grant_edit = {
    "form_class" : GrantForm,
    "template_name" : "verbena/grants/grant_form.html",
}

grant_view = {
    "queryset" : Grant.objects.all(),
    "template_name" : "verbena/grants/grant_detail.html",
}

urlpatterns = patterns("",
    url(r"^$", object_list, grant_list, name="grant_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, grant_view, name="grant_view"),
    ##url(r"^apply/$", create_object, grant_add, name="grant_add"),
    url(r"^apply/$", add_grant, name="grant_add"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, grant_edit, name="grant_edit"),
)
