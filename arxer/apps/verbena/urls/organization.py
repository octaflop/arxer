from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import Organization
from verbena.forms import OrganizationForm, LocationForm
from verbena.views import add_organization

tdir = "verbena/organization/"

org_list = {
    "queryset" : Organization.objects.all(),
    "template_name" : "%s%s" % (tdir, "organization_list.html")
}

org_add = {
    "model" : Organization,
    "login_required" : True,
    "template_name" : "%s%s" % (tdir, "organization_form.html")
}

org_edit = {
    "form_class" : OrganizationForm,
    "login_required" : True,
    "template_name" : "%s%s" % (tdir, "organization_form.html"),
    "slug_field" : "org_slug",
}

org_detail = {
    "queryset" : Organization.objects.all(),
    "template_name" : "%s%s" % (tdir, "organization_detail.html"),
    "slug_field" : "org_slug",
}

urlpatterns = patterns("",
    url(r"^$", object_list, org_list, name="org_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, org_detail, name="org_view"),
    #url(r"^add/$", create_object, org_add, name="org_add"),
    url(r"^add/$", add_organization, name="org_add"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, org_edit, name="org_edit"),
)

