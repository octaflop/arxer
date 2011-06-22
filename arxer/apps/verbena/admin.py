# the admin views
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ajax_select import make_ajax_form

from verbena.models import Student, Faculty, NewsRelease, Location, Project,\
    VolunteerOpportunity, Organization, Workshop, ActionGroup, Grant,\
    Navigation, Member, Chunk, StaffBio

#class MemberAdmin(UserAdmin):
#    pass

class MemberAdmin(admin.ModelAdmin):
    pass

class StaffBioAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ChunkAdmin(admin.ModelAdmin):
    list_display = ('slug',)

class NavigationAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'weight',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('member', 'studying','comp_year',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('member', 'in_faculty',)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'leader', 'about', 'website',)
    prepopulated_fields = {'org_slug': ('title',)}
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

class EventAdmin(admin.ModelAdmin):
    pass

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

admin.site.register(StaffBio, StaffBioAdmin)
admin.site.register(Chunk, ChunkAdmin)
# akin to adding !important, but for some "AlreadyRegistered" error.
#admin.site.unregister(Project)
admin.site.register(Project, ProjectAdmin)

#admin.site.unregister(VolunteerOpportunity)
admin.site.register(VolunteerOpportunity, VolunteerOpportunityAdmin)

#admin.site.unregister(Workshop)
admin.site.register(Workshop, WorkshopAdmin)

#admin.site.unregister(Organization)
admin.site.register(Organization, OrganizationAdmin)

#admin.site.unregister(Location)
admin.site.register(Location, LocationAdmin)

#admin.site.unregister(NewsRelease)
admin.site.register(NewsRelease, NewsReleaseAdmin)

#admin.site.unregister(Student)
admin.site.register(Student, StudentAdmin)

#admin.site.unregister(Faculty)
admin.site.register(Faculty, FacultyAdmin)

#admin.site.unregister(ActionGroup)
admin.site.register(ActionGroup, ActionGroupAdmin)

#admin.site.unregister(Grant)
admin.site.register(Grant, GrantAdmin)

#admin.site.unregister(Navigation)
admin.site.register(Navigation, NavigationAdmin)

#admin.site.unregister(Member)
admin.site.register(Member, MemberAdmin)
