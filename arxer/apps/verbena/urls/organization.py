from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from verbena.models import Organization

org_list = {
    "queryset" : Organization.objects.all(),
}

urlpatterns = patterns("",
    url(r"^$", object_list, org_list, name="org_home"),
)

