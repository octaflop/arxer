from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.views import join_actiongroup, leave_actiongroup
from verbena.models import Student, GeneralMember, Faculty
from verbena.forms import StudentForm, FacultyForm, GeneralMemberForm

# all profiles
member_list = {
    "queryset"  : GeneralMember.objects.all()
}

student_list = {
    "queryset"  : Student.objects.all()
}

faculty_list = {
    "queryset"  : Faculty.objects.all()
}

urlpatterns = patterns("",
    url(r"^$", object_list, member_list, name="member_list"),
    url(r"students$", object_list, student_list, name="student_list"),
    url(r"students/(?P<slug>[-\w]+)$", object_detail, student_list, name="student_view"),
    url(r"faculty$", object_list, faculty_list, name="faculty_list"),
    url(r"faculty/(?P<slug>[-\w]+)$", object_detail, faculty_list,  name="faculty_view"),
    )
