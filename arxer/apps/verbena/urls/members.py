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

student_add = {
    "form_class" : StudentForm,
    "login_required": True,
}

faculty_list = {
    "queryset"  : Faculty.objects.all()
}

faculty_add = {
    "form_class" : FacultyForm,
    "login_required": True,
}

urlpatterns = patterns("",
    url(r"^$", object_list, member_list, name="member_list"),
    url(r"students$", object_list, student_list, name="student_list"),
    url(r"students/add", create_object, student_add,  name="student_add"),
    url(r"students/(?P<slug>[-\w]+)$", object_detail, student_list, name="student_view"),
    url(r"students/(?P<slug>[-\w]+)/edit$", update_object, student_add,
        name="student_edit"),
    url(r"faculty$", object_list, faculty_list, name="faculty_list"),
    url(r"faculty/add", create_object, faculty_add,  name="faculty_add"),
    url(r"faculty/(?P<slug>[-\w]+)$", object_detail, faculty_list,  name="faculty_view"),
    url(r"faculty/(?P<slug>[-\w]+)/edit$", update_object, faculty_add,
        name="faculty_edit"),
    )
