from django import forms
from django.contrib import admin

from tinymce.widgets import TinyMCE
from emencia.django.newsletter.models import Newsletter
from emencia.django.newsletter.admin import NewsletterAdmin


class NewsletterTinyMCEForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 150, 'rows': 80}))

    class Meta:
        model = Newsletter

class NewsletterTinyMCEAdmin(NewsletterAdmin):
    form = NewsletterTinyMCEForm

admin.site.unregister(Newsletter)
admin.site.register(Newsletter, NewsletterTinyMCEAdmin)
