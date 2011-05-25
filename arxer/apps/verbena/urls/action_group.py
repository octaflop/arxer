from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.views import join_actiongroup, leave_actiongroup, add_actiongroup
from verbena.models import ActionGroup
from verbena.forms import ActionGroupForm

act_list = {
    "queryset"  : ActionGroup.objects.all(),
    "template_name": "verbena/act_group/actiongroup_list.html",
}

act_add = {
    "form_class" : ActionGroupForm,
    "login_required": True,
    "template_name": "verbena/act_group/actiongroup_form.html",
}

act_edit = {
    "form_class" : ActionGroupForm,
    "login_required": True,
    "template_name": "verbena/act_group/actiongroup_form.html",
}

act_view = {
    "queryset"  : ActionGroup.objects.all(),
    "template_name" : "verbena/act_group/actiongroup_detail.html",
}

urlpatterns = patterns("",
    url(r"^$", object_list, act_list, name="act_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, act_view, name="act_view"),
    url(r"^(?P<slug>[-\w]+)/join$", join_actiongroup, act_list, name="act_join"),
    url(r"^(?P<slug>[-\w]+)/leave$", leave_actiongroup, act_list, name="act_leave"),
    #url(r"^add/$", create_object, act_add, name="act_add"),
    url(r"^add/$", add_actiongroup, act_add, name="act_add"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, act_edit, name="act_edit"),
    )
