from modeltranslation.translator import translator, TranslationOptions
from arx.models import Project, Page, ActionGroup, Student, Faculty, Organization

class StudentTranslationOptions(TranslationOptions):
    fields = ('studying',)

class FacultyTranslationOptions(TranslationOptions):
    fields = ('faculty',)

class ActionGroupTranslationOptions(TranslationOptions):
    fields = ('group_name',)

class PageTranslationOptions(TranslationOptions):
    fields = ('title',)

class ProjectTranslationOptions(TranslationOptions):
    fields = ('title',)

class OrganizationTranslationOptions(TranslationOptions):
    fields = ('title',)

#class ProfileTranslationOptions(TranslationOptions):
#    fields = ('name', 'about', 'location',)

translator.register(Project, ProjectTranslationOptions)
translator.register(Faculty, FacultyTranslationOptions)
translator.register(Student, StudentTranslationOptions)
translator.register(Organization, OrganizationTranslationOptions)
translator.register(ActionGroup, ActionGroupTranslationOptions)
translator.register(Page, PageTranslationOptions)
