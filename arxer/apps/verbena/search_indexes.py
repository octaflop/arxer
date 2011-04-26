from haystack.indexes import *
from haystack import site
from verbena.models import Project, ActionGroup, Organization, Student, Faculty, GeneralMember

class ProjectIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

class ActionGroupIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

class OrganizationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

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
