from haystack.indexes import *
from haystack import site
from verbena.models import Project, ActionGroup, Organization, Student,\
Faculty, GeneralMember, Event

class ProjectIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    project_description = CharField(model_attr='project_description')
    title_auto = EdgeNgramField(model_attr='title')

class ActionGroupIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title_auto = EdgeNgramField(model_attr='title')

class OrganizationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    about = CharField(model_attr='about')
    title_auto = EdgeNgramField(model_attr='title')

"""
TODO: Make this differentiate between future and previous events in the search
"""
class EventIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title_auto = EdgeNgramField(model_attr='title')

class GeneralMemberIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

class StudentIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

class FacultyIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Project, ProjectIndex)
site.register(ActionGroup, ActionGroupIndex)
site.register(Organization, OrganizationIndex)
site.register(GeneralMember, GeneralMemberIndex)
site.register(Student, StudentIndex)
site.register(Faculty, FacultyIndex)
site.register(Event, EventIndex)
