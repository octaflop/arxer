from haystack import indexes
from verbena.models import Project, ActionGroup, Organization, Student,\
Faculty, Member, Event

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    project_description = indexes.CharField(model_attr='project_description')
    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Project

class ActionGroupIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return ActionGroup

class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    about = indexes.CharField(model_attr='about')
    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Organization

"""
TODO: Make this differentiate between future and previous events in the search
"""
class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Event

class MemberIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Member

class StudentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Student

class FacultyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Faculty

