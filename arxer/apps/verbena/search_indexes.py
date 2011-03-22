from haystack.indexes import *
from haystack import site
from verbena.models import Project, ActionGroup

class ProjectIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

class ActionGroupIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

site.register(Project, ProjectIndex)
site.register(ActionGroup, ActionGroupIndex)
