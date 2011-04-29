from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.models import VolunteerOpportunity
from verbena.forms import VolunteerOpForm
from verbena.views import join_vop, leave_vop

volunteer_list = {
    "queryset" : VolunteerOpportunity.objects.all(),
}

volunteer_add = {
    "model" : VolunteerOpportunity,
    "login_required" : True,
}

volunteer_edit = {
    "form_class" : VolunteerOpForm,
    "login_required" : True,
}

urlpatterns = patterns("",
    url(r"^$", object_list, volunteer_list, name="volunteer_home"),
    url(r"^(?P<slug>[-\w]+)$", object_detail, volunteer_list, name="volunteer_view"),
    url(r"^(?P<slug>[-\w]+)/join$", join_vop, volunteer_list, name="volunteer_join"),
    url(r"^(?P<slug>[-\w]+)/leave$", leave_vop, volunteer_list,
        name="volunteer_leave"),
    url(r"^add/$", create_object, volunteer_add, name="volunteer_add"),
    url(r"^(?P<slug>[-\w]+)/edit$", update_object, volunteer_edit,
        name="volunteer_edit"),
)

