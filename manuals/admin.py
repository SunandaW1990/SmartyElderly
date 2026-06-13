'''
from django.contrib import admin
from django import forms
from .models import Manual
from taggit.forms import TagWidget
from django.forms import NumberInput
from django.db import models

# Register your models here.
class ManualAdminForm(forms.ModelForm):
    class Meta:
        model = Manual
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class ManualAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'img_url', 'is_course', 'course_url', 'is_active', 'creation_date')
    list_display_links = ('id', 'name')
    #list_filter = ('name', 'is_course')
    list_editable = ('is_course', 'is_active',)
    search_fields = ('name', 'is_course',)
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
admin.site.register(Manual, ManualAdmin)
'''