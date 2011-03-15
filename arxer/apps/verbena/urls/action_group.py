from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from verbena.models import ActionGroup

act_list = {
    "queryset"  : ActionGroup.objects.all(),
}

urlpatterns = patterns("",
    url(r"^$", object_list, act_list, name="act_home"),
    )
