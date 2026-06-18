from django.contrib import admin
from django import forms
from .models import Story
from taggit.forms import TagWidget
from django.forms import NumberInput
from django.db import models

# Register your models here.
class StoryAdminForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = '__all__'
        widgets = {
            'services': TagWidget(attrs={
                "style": "width: 100px"
            }),
        }

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'content', 'category', 'speech_url', 'is_published', 'is_anonymous', 'creation_date')
    list_display_links = ('id', 'user')
    #list_filter = ('doctor', 'services')
    list_editable = ('title', 'content', 'category', 'speech_url', 'is_published', 'is_anonymous' )
    search_fields = ('title', 'content', 'category')
    list_per_age = 25                
    #formfield_overrides = {
    #    models.IntegerField: {
    #        "widget": forms.NumberInput(attrs={"size":"10"})
    #    }
    #}      

    """
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("services")

    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.services.all()]) or "No tags"
    
    tag_list.short_description = "Services"
    """
admin.site.register(Story, StoryAdmin)