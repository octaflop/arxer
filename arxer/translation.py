from modeltranslation.translator import translator, TranslationOptions
from arx.models import Project

class ProjectTranslationOptions(TranslationOptions):
    fields = ('title',)

#class ProfileTranslationOptions(TranslationOptions):
#    fields = ('name', 'about', 'location',)

translator.register(Project, ProjectTranslationOptions)
