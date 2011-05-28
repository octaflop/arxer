from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.views import join_actiongroup, leave_actiongroup, list_all_members
from verbena.models import Student, GeneralMember, Faculty, Member
from verbena.forms import StudentForm, FacultyForm, GeneralMemberForm


memtemp = "verbena/members/"
# all profiles
member_list = {
    #"queryset"  : GeneralMember.objects.all()
    "queryset"  : Member.objects.all(),
    "template_name" : "%s%s" % (memtemp, "member_list.html"),
}

student_list = {
    "queryset"  : Student.objects.all(),
    "template_name" : "%s%s" % (memtemp, "member_list.html"),
}

student_add = {
    "form_class" : StudentForm,
    #"login_required": True,
    "template_name" : "%s%s" % (memtemp, "member_form.html"),
}

faculty_list = {
    "queryset"  : Faculty.objects.all(),
    "template_name" : "%s%s" % (memtemp, "member_list.html"),
}

faculty_add = {
    "form_class" : FacultyForm,
    "login_required": True,
    "template_name" : "%s%s" % (memtemp, "member_form.html"),
}

member_view = {
    "queryset" : Member.objects.all(),
    "template_name" : "%s%s" % (memtemp, "member_detail.html"),
}

urlpatterns = patterns("",
    ##url(r"^$", object_list, member_list, name="member_list"),
    url(r"^$", list_all_members, name="member_list"),
    url(r"(?P<slug>[-\w]+)$", object_detail, member_view, name="member_view"),
    url(r"students$", object_list, student_list, name="student_list"),
    url(r"students/add", create_object, student_add, name="student_add"),
    url(r"students/(?P<slug>[-\w]+)$", object_detail, member_view, name="student_view"),
    url(r"students/(?P<slug>[-\w]+)/edit$", update_object, student_add,
        name="student_edit"),
    url(r"faculty$", object_list, faculty_list, name="faculty_list"),
    url(r"faculty/add", create_object, faculty_add,  name="faculty_add"),
    url(r"faculty/(?P<slug>[-\w]+)$", object_detail, member_view, name="faculty_view"),
    url(r"faculty/(?P<slug>[-\w]+)/edit$", update_object, faculty_add,
        name="faculty_edit"),
)
