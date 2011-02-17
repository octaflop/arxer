from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from arx.models import Project

class ProjectAdmin(TranslationAdmin):
    list_display = ('title',)

admin.site.register(Project, ProjectAdmin)
