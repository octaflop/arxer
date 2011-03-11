# the admin views
from django.contrib import admin

from verbena.models import Student, Faculty, NewsRelease, Location, Project,\
    VolunteerOpportunity, Organization, Workshop

class StudentAdmin(admin.ModelAdmin):
    list_display = ('studying','comp_year',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('in_faculty',)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'location', 'website',)

class NewsReleaseAdmin(admin.ModelAdmin):
    list_display = ('content', 'datetime',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('place', 'latitude', 'longitude',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','approval_status','progress_status',)
    prepopulated_fields = {'slug': ('title',)}

class WorkshopAdmin(admin.ModelAdmin):
    display_inline = ('members',)
    prepopulated_fields = {'slug': ('title',)}

class VolunteerOpportunityAdmin(admin.ModelAdmin):
    #list_display = ('organization','volunteers',)
    display_inline = ('organization',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Project, ProjectAdmin)
admin.site.register(VolunteerOpportunity, VolunteerOpportunityAdmin)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(NewsRelease, NewsReleaseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Organization, OrganizationAdmin)
