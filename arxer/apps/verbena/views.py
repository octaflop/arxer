# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
# other imports
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.simple import direct_to_template as render
from django.core.urlresolvers import reverse
from verbena.models import Organization, Project, VolunteerOpportunity,\
    Member, ActionGroup, Research, Student, Faculty, Event,\
    StudentProject, Grant
from verbena.forms import ProjectForm, OrganizationForm, LocationForm,\
    StudentForm, UserForm, MemberForm, ActionGroupForm, AvatarForm,\
    FacultyForm, GrantForm, EventForm
from photologue.models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile
from verbena.models import Organization, Location, Project
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.core.urlresolvers import reverse
from django.contrib import messages
#haystack
from haystack.query import SearchQuerySet
from django.utils import simplejson
#from pinax.apps.account.forms import SignupForm
from verbena.forms import UserForm
import datetime
#from tinymce.views import render_to_link_list

#def mcefilebrowser(request):
#    objects = Photos.objects.all()
   # link_list = [(unicode(obj), obj.get_absolute_url()) for obj in objects]
   # return render_to_link_list(link_list)

def ev_list(request, *args, **kwargs):
    """
    list all events
    """
    try:
        events = Event.objects.filter(end_date__gte=datetime.datetime.now())
    except Event.DoesNotExist:
        events = {}
    ret = dict(events=events)
    return render(request, 'verbena/events/event_list.html', ret)

def compile_search(results):
    resultlist = [r.title_auto for r in results]
    encoder = simplejson.JSONEncoder()
    resp = encoder.encode(resultlist)
    return resp

# Grant application
@login_required
def add_grant(request, *args, **kwargs):
    """
    Add the current user as the applicant for the grant
    """
    if request.POST:
        data = request.POST
        grantform = GrantForm(data=data)
        if grantform.is_valid():
            grant = grantform.save(commit=False)
            grant.applicant = request.user.member
            try:
                grant.save()
            except:
                return HttpResponse(status=500)
            return redirect(grant.get_absolute_url())
    else:
        grantform = GrantForm()
    ret = dict(form=grantform)
    return render(request, 'verbena/grants/grant_form.html', ret)

#haystack search
# Search suggestions
def suggestion(request):
    # from haystack.query import SearchQuerySet
    word = request.GET['term']
    results = SearchQuerySet().autocomplete(title_auto=word)
    resp = compile_search(results)
    return HttpResponse(resp, content_type='application/x-javascript')

def edit_org(request, *args, **kwargs):
    is_me = False
    try:
        org = Organization.objects.get(org_slug=kwargs['slug'])
    except Organization.DoesNotExist:
        return HttpResponse(status=404)
    try:
        member = request.user.member
        if member == org.leader:
            is_me = True
    except AttributeError:
        is_me = False
    kwargs['extra_context'] = is_me
    return update_object(request, *args, **kwargs)

def act_detail(request, *args, **kwargs):
    """
        List details for org, show if user is in or not
    """
    is_in = False
    try:
        act = ActionGroup.objects.get(slug=kwargs['slug'])
    except ActionGroup.DoesNotExist:
        return HttpResponse(status=404)
    try:
        member = request.user.member
        if member in act.supporters.all():
            is_in = True
    except AttributeError:
        is_in = False
    ret = dict(object=act, is_in=is_in)
    return render(request, 'verbena/act_group/actiongroup_detail.html', ret)

# Add an event to a 
def add_event(request, slug, *args, **kwargs):
    data = request.POST or None
    ag = ActionGroup.objects.get(slug=slug)
    evform = EventForm(data=data)
    if evform.is_valid():
        ev = evform.save()
        ag.events.add(ev)
        ag.save()
    ret = dict(form=evform)
    return render(request, 'verbena/act_group/actiongroup_form_add_event.html', ret)

# model control functions
def del_member_class(old_member):
    old_org = Organization.objects.filter(leader=old_member)
    old_faculty = Faculty.objects.filter(member=old_member)
    old_student = Student.objects.filter(member=old_member)
    if old_org.exists():
        old_org.delete()
    if old_faculty.exists():
        old_faculty.delete()
    if old_student.exists():
        old_student.delete()

# Simple Wrappers
def add_faculty(request, *args, **kwargs):
    """
    Sign up a member as a faculty.
    Also "seal" the faculty into this membership by deleting old memberships
    """
    data = request.POST
    facultyform = FacultyForm(data=data)
    if facultyform.is_valid():
        faculty = facultyform.save(commit=False)
        faculty.member = request.user.member
        del_member_class(faculty.member)
        # after deleting, we finally try one more save
        try:
            faculty.save()
            messages.add_message(request, messages.SUCCESS,
                _("Successfully added %(faculty)s as faculty.") % {
                    "faculty": faculty.member.user.username
                }
            )
        except:
            return HttpResponse(status=500)
        return redirect(faculty.get_absolute_url())
    ret = dict(form=facultyform)
    return HttpResponse(request, 'verbena/members/faculty_form.html', ret)

def faculty_edit(request, *args, **kwargs):
    """ A wrapper to pull up a student and edit them """
    faculty = Faculty.objects.get(member__slug=kwargs['slug'])
    is_me = False
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if faculty.member.user == request.user:
            is_me=True
        if form.is_valid():
            new_faculty = form.save(commit=False)
            if is_me:
                new_faculty.member = request.user.member
                faculty.delete()
                new_faculty.save()
                return redirect(faculty.get_absolute_url())
            else:
                return HttpResponse(status=403)
    else:
        form = FacultyForm(instance=faculty)
    ret = dict(object=faculty, form=form, is_me=is_me)
    return render(request, 'verbena/members/faculty_form.html', ret)

def faculty_detail(request, *args, **kwargs):
    """ A wrapper to see if a faculty member is logged in as themselves """
    is_me = False
    try:
        faculty = Faculty.objects.get(member__slug=kwargs['slug'])
    except Faculty.DoesNotExist:
        return HttpResponse(status=404)
    if faculty.member.user == request.user:
        is_me = True
    ret = dict(is_me=is_me, object=faculty)
    return render(request, 'verbena/members/faculty_detail.html', ret)

# Student signup
def add_student(request, *args, **kwargs):
    """
    Sign up a member as a student.
    Also "seal" the student into this membership
    """
    data = request.POST
    studentform = StudentForm(data=data)
    if studentform.is_valid():
        student = studentform.save(commit=False)
        student.member = request.user.member
        del_member_class(student.member)
        # after deleting, we finally try one more save
        try:
            student.save()
            messages.add_message(request, messages.SUCCESS,
                _("Successfully added %(student)s as student.") % {
                    "student": student.member.user.username
                }
            )
        except:
            return HttpResponse(status=500)
        return redirect(student.get_absolute_url())
    ret = dict(form=studentform)
    return HttpResponse(request, 'verbena/members/student_form.html', ret)

def student_edit(request, *args, **kwargs):
    """ A wrapper to pull up a student and edit them """
    student = Student.objects.get(member__slug=kwargs['slug'])
    is_me = False
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if student.member.user == request.user:
            is_me=True
        if form.is_valid():
            new_student = form.save(commit=False)
            if is_me:
                new_student.member = request.user.member
                student.delete()
                new_student.save()
                return redirect(student.get_absolute_url())
            else:
                return HttpResponse(status=403)
    else:
        form = StudentForm(instance=student)
    ret = dict(object=student, form=form, is_me=is_me)
    return render(request, 'verbena/members/student_form.html', ret)

def student_detail(request, *args, **kwargs):
    """ A wrapper to see if a student is logged in as themselves """
    is_me = False
    try:
        student = Student.objects.get(member__slug=kwargs['slug'])
    except Student.DoesNotExist:
        return HttpResponse(status=404)
    if student.member.user == request.user:
        is_me = True
    ret = dict(is_me=is_me, object=student)
    return render(request, 'verbena/members/student_detail.html', ret)

# ARX
@permission_required('verbena.add_project')
def add_project(request, *args, **kwargs):
    "Add a project: must be organization"
    if request.POST:
        data = request.POST
        projform = ProjectForm(data=data)
        if projform.is_valid():
            proj = projform.save(commit=False)
            try:
                organization =\
                    Organization.objects.get(leader=request.user.member)
            except Organization.DoesNotExist:
                return HttpResponse(status=403)
            proj.organization = organization
            proj.save()
            return redirect(proj.get_absolute_url())
    else:
        projform = ProjectForm()
    #return create_object(*args, **kwargs)
    ret = dict(form=projform)
    return render(request, 'verbena/arx/arx_form.html', ret)

@permission_required('verbena.change_project')
def change_project(*args, **kwargs):
    "Change the project: must be owner"
    return update_object(*args, **kwargs)

# all leave permissions are == to join permissions
@permission_required('verbena.join_project')
def leave_project(request, *args, **kwargs):
    "Leave a volunteer opportunity"
    volunteer = Member.objects.get(user=request.user)
    res = Research.objects.get(slug=kwargs['slug'])
    res.volunteers.remove(volunteer)
    try:
        res.save()
        messages.add_message(request, messages.SUCCESS,
                _("Successfully left %(op)s.") % {
                    "op": res.title,
                }
            )
    except DoesNotExist:
        return HttpResponse(status=500)
    return redirect(res.get_absolute_url())

@permission_required('verbena.join_project')
def join_project(*args, **kwargs):
    "join a research project"
    project = Project.objects.get(slug=kwargs['slug'])
    return update_object(*args, **kwargs)

@permission_required('verbena.change_research')
def change_research(*args, **kwargs):
    """
    join a research project
    """
    return update_object(*args, **kwargs)

# Heavy lifting
def member_signup(request, *args, **kwargs):
    """
    Signup a new member
    Add the member to a group-type if necessary
    """
    data = request.POST or None
    form = UserForm(data=data)
    mdata = request.FILES or None
    avatar_form = AvatarForm(data, mdata)
    if avatar_form.is_valid() and form.is_valid():
        user = form.save()
        avatar = avatar_form.save()
        user.member.avatar = avatar
        try:
            user.member.save()
            form.login(request, user)
            messages.add_message(request, messages.SUCCESS,
                    _("Successfully added %(member)s as a member.") % {
                        "member": user.username
                    }
                )
            return redirect(user.member.get_absolute_url())
        except:
            return redirect("member_signup")
    ret = dict(form=form,avform=avatar_form)
    return render(request, 'verbena/members/signup.html', ret)

@login_required
def member_avatar_edit(request, *args, **kwargs):
    """
    edit or add an avatar to the member
    """
    data = request.POST or None
    file_data = request.FILES
    form = AvatarForm(data, file_data)
    if form.is_valid():
        member = request.user.member
        member.avatar = form.save()
        try:
            member.save()
            messages.add_message(request, messages.SUCCESS,
                    _("Successfully added an avatar")
                )
            return redirect(member.get_absolute_url())
        except:
            return HttpResponse(status=404)
    ret = dict(form=form)
    return render(request, 'verbena/members/avatar_edit.html', ret)

def list_all_members(request, *args, **kargs):
    """
    List all of the members
    """
    ##import pdb; pdb.set_trace()
    ##member_list = []
    mems = Member.objects.all()
    #for mem in mems:
    #    member_list.append(mem)
    """
    orgs = Organization.objects.all()
    for org in orgs:
        member_list.append(org)
    students = Student.objects.all()
    for student in students:
        member_list.append(student)
    facultys = Faculty.objects.all()
    for faculty in facultys:
        member_list.append(faculty)
    """
    ret = dict(object_list=mems)
    return render(request, 'verbena/members/member_list.html', ret)

# Volunteer opportunities
@login_required
@permission_required('verbena.join_volunteer')
def join_vop(request, *args, **kwargs):
    """
    Join a volunteer opportunity: must be a general member
    """
    volunteer = Member.objects.get(user=request.user)
    op = VolunteerOpportunity.objects.get(slug=kwargs['slug'])
    op.volunteers.add(volunteer)
    try:
        op.save()
        messages.add_message(request, messages.SUCCESS,
                _("Successfully joined %(op)s.") % {
                    "op": op.title,
                }
            )
    except:
        return HttpResponse(status=500)
    return redirect(op.get_absolute_url())
    #return object_detail(request, *args, **kwargs)

@login_required
@permission_required('verbena.join_volunteer')
def leave_vop(request, *args, **kwargs):
    """
    Leave a volunteer opportunity
    """
    volunteer = Member.objects.get(user=request.user)
    op = VolunteerOpportunity.objects.get(slug=kwargs['slug'])
    op.volunteers.remove(volunteer)
    try:
        op.save()
    except:
        return HttpResponse(status=500)
    return redirect(op.get_absolute_url())

# Action Group
@login_required
@permission_required('verbena.add_actiongroup')
def add_actiongroup(request, *args, **kwargs):
    """
    Create an action group and set up logged-in user as the leader
    """
    data = request.POST or None
    agform = ActionGroupForm(data=data)
    mdata = request.FILES or None
    avatar_form = AvatarForm(data, mdata)
    if agform.is_valid() and avatar_form.is_valid():
        new_ag = agform.save(commit=False)
        user = request.user.member
        try:
            new_ag.leader = user
##            import pdb; pdb.set_trace()
            portrait = avatar_form.save()
            new_ag.portrait = portrait
            try:
                new_ag.save()
                messages.add_message(request, messages.SUCCESS,
                    _("Successfully added %(ag)s to action groups.") % {
                        "ag": new_ag.title
                    }
                )
                return HttpResponseRedirect(new_ag.get_absolute_url())
            except:
                return HttpResponse(status=500)
        except Member.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponseRedirect(new_ag.get_absolute_url())
    ret = dict(form=agform, avform=avatar_form)
    return render(request, 'verbena/act_group/actiongroup_form.html', ret)

@login_required
@permission_required('verbena.join_actiongroup')
def join_actiongroup(request, *args, **kwargs):
    "Join an action group: must be a general member"
    member = request.user.member
    try:
        ag = ActionGroup.objects.get(slug=kwargs['slug'])
    except ActionGroup.DoesNotExist:
        return HttpResponse(status=404)
    ag.supporters.add(member)
    try:
        ag.save()
        messages.add_message(request, messages.SUCCESS,
                _("Successfully joined %(ag)s.") % {
                    "ag": ag.title,
                }
            )
    except:
        return HttpResponse(status=500)
    return redirect(ag.get_absolute_url())

@login_required
@permission_required('verbena.join_actiongroup')
def leave_actiongroup(request, *args, **kwargs):
    "Leave an action group: must be a general member"
    member = request.user.member
    try:
        ag = ActionGroup.objects.get(slug=kwargs['slug'])
    except ActionGroup.DoesNotExist:
        return HttpResponse(status=404)
    ag.supporters.remove(member)
    try:
        ag.save()
        messages.add_message(request, messages.SUCCESS,
                _("Successfully left %(ag)s.") % {
                    "ag": ag.title,
                }
            )
    except:
        return HttpResponse(status=500)
    return redirect(ag.get_absolute_url())

@login_required
def edit_action_group(request, slug, *args, **kwargs):
    data = request.POST or None
    mdata = request.FILES or None
    try:
        ag = ActionGroup.objects.get(slug=slug)
        if ag.leader != request.user.member:
            messages.add_message(request, messages.ERROR,
                _("You do not have permission to edit %(ag)s.") % {
                    "ag": ag.title,
                }
            )
            return HttpResponse(status=403)
    except ActionGroup.DoesNotExist:
        return HttpResponse(status=404)
    avform = AvatarForm(data, mdata, instance=ag.portrait)
    agform = ActionGroupForm(data, instance=ag)
    ret = dict(form=agform, avform=avform)
    if agform.is_valid() and avform.is_valid():
        agform.save(commit=False)
        av = avform.save()
        agform.portrait = av
        ag = agform.save()
        messages.add_message(request, messages.SUCCESS,
                _("Successfully edited %(ag)s.") % {
                    "ag": ag.title,
                }
            )
        return redirect(ag.get_absolute_url())
    return render(request, "verbena/act_group/actiongroup_form.html", ret)

# Organizations
def add_organization(request, *args, **kwargs):
    if request.POST:
        data = request.POST
        userform = UserForm(data=data)
        orgform = OrganizationForm(data=data)
        location = {}
        if orgform.is_valid():
            new_organization = orgform.save(commit=False)
            if not request.user == AnonymousUser:
                if userform.is_valid():
                    if userform.cleaned_data['password'] == userform.cleaned_data['passconf']:
                        new_user = User.objects.create_user(
                            userform.cleaned_data['username'],
                            userform.cleaned_data['email'],
                            userform.cleaned_data['password'])
            else:
                new_user = request.user
                try:
                    del_member_class(new_user.member)
                except:
                    pass
            new_organization.leader = new_user.member
            new_organization.save()
            new_organization.save()
            messages.add_message(request, messages.SUCCESS,
                _("Successfully added %(org)s as organization.") % {
                    "org": new_organization.leader.user.username
                }
            )
            return HttpResponseRedirect(new_organization.get_absolute_url())
    else:
        userform = UserForm()
        orgform = OrganizationForm()
    ret = dict(userform=userform, orgform=orgform)
    return render(request, 'verbena/organization/organization_form.html', ret)

