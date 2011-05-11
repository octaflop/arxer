from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Organization
from verbena.forms import OrganizationForm, LocationForm
from verbena.views import add_organization

org_list = {
    "queryset" : Organization.objects.all(),
}

org_add = {
    "model" : Organization,
    "login_required" : True,
}

org_edit = {
    "form_class" : OrganizationForm,
    "login_required" : True,
}

urlpatterns = patterns("",
    url(r"^$", object_list, org_list, name="org_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, org_list, name="org_view"),
    #url(r"^add/$", create_object, org_add, name="org_add"),
    url(r"^add/$", add_organization, name="org_add"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, org_edit, name="org_edit"),
)

