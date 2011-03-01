# the admin views
from django.contrib import admin

from verbena.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Project, ProjectAdmin)
