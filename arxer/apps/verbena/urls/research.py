from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Research
from verbena.forms import ResearchForm

# similar to the action-group

res_list = {
    "queryset" : Research.objects.all(),
    "template_name" : "verbena/research/research_list.html",
}

res_add = {
    "model" : Research,
    "login_required" : True,
    "template_name" : "verbena/research/research_form.html",
}

res_edit = {
    "form_class" : ResearchForm,
    "login_required": True,
    "template_name" : "verbena/research/research_form.html",
}

res_detail = {
    "queryset" : Research.objects.all(),
    "template_name" : "verbena/research/research_detail.html",
}

urlpatterns = patterns("",
    url(r"^$", object_list, res_list, name="res_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, res_detail, name="res_view"),
    ##url(r"^(?P<slug>[-\w]+)/join$", join_research, res_list, name="res_join"),
    ##url(r"^(?P<slug>[-\w]+)/leave$", leave_research, res_list, name="res_leave"),
    url(r"^add/$", create_object, res_add, name="res_add"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, res_edit, name="res_edit"),
)
