# the admin views
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from verbena.models import Student, Faculty, NewsRelease, Location, Project,\
    VolunteerOpportunity, Organization, Workshop, ActionGroup, Grant

#class StudentAdmin(UserAdmin):
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','studying','comp_year',)
    exclude = ('slug',)

#class FacultyAdmin(UserAdmin):
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('in_faculty',)
    exclude = ('slug',)

#class OrganizationAdmin(UserAdmin):
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'website',)
    prepopulated_fields = {'slug': ('name',)}
    display_inline = ('location', 'workshops',)

class NewsReleaseAdmin(admin.ModelAdmin):
    list_display = ('content', 'datetime_released',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('place', 'latitude', 'longitude',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','approval_status','progress_status',)
    prepopulated_fields = {'slug': ('title',)}

class ActionGroupAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}

class WorkshopAdmin(admin.ModelAdmin):
    display_inline = ('members',)
    prepopulated_fields = {'slug': ('title',)}
    display_inline = ('location', 'members',)

class VolunteerOpportunityAdmin(admin.ModelAdmin):
    #list_display = ('organization','volunteers',)
    display_inline = ('organization',)
    prepopulated_fields = {'slug': ('title',)}

class GrantAdmin(admin.ModelAdmin):
    display_inline = ('organization','date_applied',)
    exclude = ('date_applied',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Project, ProjectAdmin)
admin.site.register(VolunteerOpportunity, VolunteerOpportunityAdmin)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(NewsRelease, NewsReleaseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(ActionGroup, ActionGroupAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Grant, GrantAdmin)