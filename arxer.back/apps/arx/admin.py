from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from pinax.apps.profiles.models import Profile
from arx.models import Project, Page, Organization, Faculty, Student, ActionGroup

class StudentAdmin(TranslationAdmin):
    list_display = ('studying', 'comp_year',)

class FacultyAdmin(TranslationAdmin):
    list_display = ('faculty',)

class ActionGroupAdmin(TranslationAdmin):
    list_display = ('group_name',)

class PageAdmin(TranslationAdmin):
    list_display = ('title',)

class ProjectAdmin(TranslationAdmin):
    list_display = ('location','approval_status','progress_status')

class OrganizationInline(admin.TabularInline):
    model = Organization

class Profile(admin.ModelAdmin):
    inlines = [
        OrganizationInline,
    ]

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('admin',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(ActionGroup, ActionGroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Organization, OrganizationAdmin)
