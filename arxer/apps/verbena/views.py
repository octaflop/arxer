# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
# other imports
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic.simple import direct_to_template as render
from django.core.urlresolvers import reverse
from verbena.models import Organization, Project, VolunteerOpportunity,\
    Member, ActionGroup
from verbena.forms import ProjectForm, OrganizationForm, LocationForm,\
    GeneralMemberForm, StudentForm, UserForm, MemberForm
from verbena.models import Organization, Location
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.core.urlresolvers import reverse
#haystack
from haystack.query import SearchQuerySet
from django.utils import simplejson

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
@permission_required('verbena.add_project')
def add_project(*args, **kwargs):
    "Add a project: must be organization"
    return create_object(*args, **kwargs)

@permission_required('verbena.change_project')
def change_project(*args, **kwargs):
    "Change the project: must be owner"
    return update_object(*args, **kwargs)

@permission_required('verbena.add_research')
def join_research(*args, **kwargs):
    "join a research project"
    return update_object(*args, **kwargs)

@permission_required('verbena.change_research')
def change_research(*args, **kwargs):
    "join a research project"
    return update_object(*args, **kwargs)

@permission_required('verbena.leave_research')
def leave_research(request, *args, **kwargs):
    "Leave a volunteer opportunity"
    volunteer = Member.objects.get(profile__user=request.user)
    res = Research.objects.get(slug=kwargs['slug'])
    res.volunteers.remove(volunteer)
    try:
        res.save()
    except:
        return HttpResponse(status=500)
    return redirect(res.get_absolute_url())



# Heavy lifting
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
    volunteer = Member.objects.get(profile__user=request.user)
    op = VolunteerOpportunity.objects.get(slug=kwargs['slug'])
    op.volunteers.remove(volunteer)
    try:
        op.save()
    except:
        return HttpResponse(status=500)
    return redirect(op.get_absolute_url())

@login_required
@permission_required('verbena.join_actiongroup')
def join_actiongroup(request, *args, **kwargs):
    "Join an action group: must be a general member"
    member = Member.objects.get(profile__user=request.user)
    ag = ActionGroup.objects.get(slug=kwargs['slug'])
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
    member = Member.objects.get(profile__user=request.user)
    ag = ActionGroup.objects.get(slug=kwargs['slug'])
    ag.supporters.remove(member)
    try:
        ag.save()
    except:
        return HttpResponse(status=500)
    return redirect(ag.get_absolute_url())

def add_organization(request, *args, **kwargs):
    data = request.POST or None
    locform = LocationForm(data=data)
    orgform = OrganizationForm(data=data)
    userform = UserForm(data=data)
    location = {}
    if locform.is_valid() and orgform.is_valid() and userform.is_valid():
        new_location = locform.save()
        new_organization = orgform.save(commit=False)
        new_organization.location = new_location
        if userform.cleaned_data['password'] == userform.cleaned_data['passconf']:
            new_user = User.objects.create_user(
                userform.cleaned_data['username'],
                userform.cleaned_data['email'],
                userform.cleaned_data['password'])
            ## The profile is not implemented! TK
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
    return render(request, 'verbena/organization_form.html', ret)
#            {'locform':locform, 'orgform':orgform, 'location':location})

