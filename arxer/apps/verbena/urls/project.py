from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Project
from verbena.forms import ProjectForm
from verbena.views import add_project, change_project

proj_list = {
    "queryset"  : Project.objects.all(),
}

proj_edit = {
    "form_class" : ProjectForm,
}

urlpatterns = patterns("",
    url(r"^$", object_list, proj_list, name="project_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, proj_list, name="project_view"),
    #url(r"^apply/$", create_object, proj_edit, name="project_add"),
    url(r"^apply/$", add_project, proj_edit, name="project_add"),
    #url(r"^(?P<slug>[-\w]+)/edit$", update_object, proj_edit, name="project_edit"),
    url(r"^(?P<slug>[-\w]+)/edit$", change_project, proj_edit, name="project_edit"),
)
