from django.contrib import admin

from rose.models import FrontPageSlide, ARXSlide, Slide

class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'link', 'weight')
    prepopulated_fields = {'slug': ('title',)}

class FrontPageSlideAdmin(SlideAdmin):
    pass

class ARXSlideAdmin(SlideAdmin):
    pass

admin.site.register(ARXSlide, ARXSlideAdmin)
admin.site.register(FrontPageSlide, FrontPageSlideAdmin)
admin.site.register(Slide, SlideAdmin)
