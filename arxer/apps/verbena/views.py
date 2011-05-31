# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
# other imports
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.simple import direct_to_template as render
from django.core.urlresolvers import reverse
from verbena.models import Organization, Project, VolunteerOpportunity,\
    Member, ActionGroup, Research, Student, Faculty, Event,\
    StudentProject
from verbena.forms import ProjectForm, OrganizationForm, LocationForm,\
    StudentForm, UserForm, MemberForm, ActionGroupForm
from verbena.models import Organization, Location, Project
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.core.urlresolvers import reverse
#haystack
from haystack.query import SearchQuerySet
from django.utils import simplejson
import datetime

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

#haystack search
# Search suggestions
def suggestion(request):
    # from haystack.query import SearchQuerySet
    word = request.GET['term']
    results = SearchQuerySet().autocomplete(title_auto=word)
    resp = compile_search(results)
    return HttpResponse(resp, content_type='application/x-javascript')

# Simple Wrappers

# ARX
@permission_required('verbena.add_project')
def add_project(request, *args, **kwargs):
    "Add a project: must be organization"
    data = request.POST or None
    projform = ProjectForm(data=data)
    if projform.is_valid():
        try:
            projform.student_leader = Organization.objects.get(user=request.user)
        except Organization.DoesNotExist:
            return HttpResponse(status=403)
        try:
            projform.save()
        except:
            return HttpResponse(status=500)
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
    except DoesNotExist:
        return HttpResponse(status=500)
    return redirect(res.get_absolute_url())

@permission_required('verbena.join_project')
def join_project(*args, **kwargs):
    "join a research project"
    ##project = Project.objects.get(slug=request.slug)
    project = Project.objects.get(slug=kwargs['slug'])
    return update_object(*args, **kwargs)

@permission_required('verbena.change_research')
def change_research(*args, **kwargs):
    "join a research project"
    return update_object(*args, **kwargs)

# Heavy lifting
def list_all_members(request, *args, **kargs):
    """
    List all of the members
    """
    member_list = []
    genmems = Member.objects.all()
    for genmem in genmems:
        member_list.append(genmem)
    orgs = Organization.objects.all()
    for org in orgs:
        member_list.append(org)
    students = Student.objects.all()
    for student in students:
        member_list.append(student)
    facultys = Faculty.objects.all()
    for faculty in facultys:
        member_list.append(faculty)
    ret = dict(object_list=member_list)
    return render(request, 'verbena/members/generalmember_list.html', ret)

# Volunteer opportunities
@login_required
@permission_required('verbena.join_volunteer')
def join_vop(request, *args, **kwargs):
    "Join a volunteer opportunity: must be a general member"
    volunteer = Member.objects.get(user=request.user)
    op = VolunteerOpportunity.objects.get(slug=kwargs['slug'])
    op.volunteers.add(volunteer)
    try:
        op.save()
    except:
        return HttpResponse(status=500)
    return redirect(op.get_absolute_url())
    #return object_detail(request, *args, **kwargs)

@login_required
@permission_required('verbena.join_volunteer')
def leave_vop(request, *args, **kwargs):
    "Leave a volunteer opportunity"
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
    "Create an action group and set up logged-in user as the leader"
    data = request.POST or None
    agform = ActionGroupForm(data)
    if agform.is_valid():
        new_ag = agform.save(commit=False)
        ##user = Member.objects.get(profile=request.user) or None
        user = request.user.member or None
        try:
            new_ag.leader = user
            return HttpResponseRedirect(new_ag.get_absolute_url())
        except Member.DoesNotExist:
            return HttpResponse(status=404)
        return HttpResponseRedirect(new_ag.get_absolute_url())
    ret = dict(form=agform)
    return render(request, 'verbena/act_group/actiongroup_form.html', ret)

@login_required
@permission_required('verbena.join_actiongroup')
def join_actiongroup(request, *args, **kwargs):
    "Join an action group: must be a general member"
    ##member = Member.objects.get(profile=request.user)
    member = request.user.member
    try:
        ag = ActionGroup.objects.get(slug=kwargs['slug'])
    except ActionGroup.DoesNotExist:
        return HttpResponse(status=404)
    ag.supporters.add(member)
    try:
        ag.save()
    except:
        return HttpResponse(status=500)
    return redirect(ag.get_absolute_url())

@login_required
@permission_required('verbena.join_actiongroup')
def leave_actiongroup(request, *args, **kwargs):
    "Leave an action group: must be a general member"
    #member = Member.objects.get(profile=request.user)
    member = request.user.member
    try:
        ag = ActionGroup.objects.get(slug=kwargs['slug'])
    except ActionGroup.DoesNotExist:
        return HttpResponse(status=404)
    ag.supporters.remove(member)
    try:
        ag.save()
    except:
        return HttpResponse(status=500)
    return redirect(ag.get_absolute_url())

# Organizations
def add_organization(request, *args, **kwargs):
    data = request.POST or None
    #locform = LocationForm(data=data)
    locform = None
    userform = None
    orgform = OrganizationForm(data=data)
    location = {}
    if orgform.is_valid():
        new_organization = orgform.save(commit=False)
        if not request.user:
            userform = UserForm(data=data)
            if userform.is_valid():
                if userform.cleaned_data['password'] == userform.cleaned_data['passconf']:
                    new_user = User.objects.create_user(
                        userform.cleaned_data['username'],
                        userform.cleaned_data['email'],
                        userform.cleaned_data['password'])
        else:
            new_user = request.user
        new_organization.user = new_user
        new_organization.save()
        # JS Map information
        location = {
            "latitude": new_location.latitude,
            "longitude": new_location.longitude,
            "place": new_location.place
        }
        return HttpResponseRedirect(new_organization.get_absolute_url())
    ret = dict(userform=userform, locform=locform, orgform=orgform, location=location)
    return render(request, 'verbena/organization/organization_form.html', ret)

