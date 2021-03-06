from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from verbena.views import join_actiongroup, leave_actiongroup,\
    list_all_members, member_signup, member_avatar_edit,\
    add_student, student_detail, student_edit,\
    add_faculty, faculty_edit, faculty_detail
from verbena.models import Student, Faculty, Member
from verbena.forms import StudentForm, FacultyForm

memtemp = "verbena/members/"
# all profiles
member_list = {
    "queryset"  : Member.objects.all(),
    "template_name" : "%s%s" % (memtemp, "generalmember_list.html"),
}

student_list = {
    "queryset"  : Student.objects.all(),
    "template_name" : "%s%s" % (memtemp, "student_list.html"),
}

student_add = {
    "form_class" : StudentForm,
    #"login_required": True,
    "template_name" : "%s%s" % (memtemp, "student_form.html"),
}

faculty_list = {
    "queryset"  : Faculty.objects.all(),
    "template_name" : "%s%s" % (memtemp, "faculty_list.html"),
}

faculty_add = {
    "form_class" : FacultyForm,
    "login_required": True,
    "template_name" : "%s%s" % (memtemp, "faculty_form.html"),
}

member_view = {
    "queryset" : Member.objects.all(),
    "template_name" : "%s%s" % (memtemp, "member_detail.html"),
}

faculty_view = {
    "queryset" : Member.objects.all(),
    "template_name" : "%s%s" % (memtemp, "faculty_detail.html"),
}

student_view = {
    ##"queryset" : Student.objects.all(),
    "queryset" : Member.objects.all(),
    "template_name" : "%s%s" % (memtemp, "student_detail.html"),
    #"slug_field" : 'member.slug',
}

urlpatterns = patterns("",
    url(r"^$", list_all_members, name="member_list"),
    url(r"signup$", member_signup, name="member_signup"),
    url(r"avatar/edit$", member_avatar_edit, name="member_avatar_edit"),
    url(r"students$", object_list, student_list, name="student_list"),
    #url(r"students/add", create_object, student_add, name="student_add"),
    url(r"students/add", add_student, student_add, name="student_add"),
    url(r"students/(?P<slug>[-\w]+)$", student_detail, name="student_view"),
    ##url(r"students/(?P<slug>[-\w]+)$", object_detail, student_view, name="student_view"),
    url(r"students/(?P<slug>[-\w]+)/edit$", student_edit,
        name="student_edit"),
    url(r"faculty$", object_list, faculty_list, name="faculty_list"),
    #url(r"faculty/add", create_object, faculty_add,  name="faculty_add"),
    url(r"faculty/add", add_faculty, faculty_add,  name="faculty_add"),
    ##url(r"faculty/(?P<slug>[-\w]+)$", object_detail, faculty_view, name="faculty_view"),
    url(r"faculty/(?P<slug>[-\w]+)$", faculty_detail, faculty_view, name="faculty_view"),
    url(r"faculty/(?P<slug>[-\w]+)/edit$", faculty_edit, faculty_add,
        name="faculty_edit"),
    url(r"(?P<slug>[-\w]+)$", object_detail, member_view, name="member_view"),
)
