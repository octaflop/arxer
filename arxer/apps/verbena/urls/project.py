from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Project
from verbena.forms import ProjectForm
from verbena.views import add_project, change_project, leave_project,\
    join_project

proj_list = {
    ##"queryset"  : Project.objects.all(),
    "queryset"  : Project.approved.all(),
    "template_name": "verbena/arx/arx_list.html",
}

proj_edit = {
    "form_class" : ProjectForm,
    "template_name": "verbena/arx/arx_form.html",
}

proj_view = {
    "queryset"  : Project.objects.all(),
    "template_name": "verbena/arx/arx_detail.html",
}

urlpatterns = patterns("",
    url(r"^$", object_list, proj_list, name="arx_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, proj_view, name="arx_view"),
    #url(r"^apply/$", create_object, proj_edit, name="project_add"),
    url(r"^add/$", add_project, proj_edit, name="arx_add"),
    url(r"^(?P<slug>[-\w]+)/join/$", join_project, proj_edit, name="arx_add"),
    url(r"^(?P<slug>[-\w]+)/leave/$", leave_project, proj_edit, name="arx_add"),
    #url(r"^(?P<slug>[-\w]+)/edit$", update_object, proj_edit, name="project_edit"),
    url(r"^(?P<slug>[-\w]+)/edit$", change_project, proj_edit, name="arx_edit"),
)
