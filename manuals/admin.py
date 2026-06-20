from django.contrib import admin
from django import forms
from .models import Manual, LifeFilm
from taggit.forms import TagWidget
from django.forms import NumberInput
from django.db import models

# Register your models here.
class ManualAdminForm(forms.ModelForm):
    class Meta:
        model = Manual
        fields = '__all__'
        widgets = {
            'services': TagWidget(attrs={
                "style": "width: 100px"
            }),
        }

class ManualAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image', 'detail_desc', 'detail_title', 'detail_title2', 
                    'explanation', 'important1', 'important2', 'important3', 'is_active', 'creation_date')
    list_display_links = ('id', 'name')
    #list_filter = ('name', 'is_course')
    list_editable = ('description', 'image', 'detail_desc', 'detail_title', 'detail_title2', 
                    'explanation', 'important1', 'important2', 'important3', 'is_active',)
    search_fields = ('name',)
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

class LifeFilmAdminForm(forms.ModelForm):
    class Meta:
        model = LifeFilm
        fields = '__all__'
        widgets = {
            'services': TagWidget(attrs={
                "style": "width: 100px"
            }),
        }

class LifeFilmAdmin(admin.ModelAdmin):
    list_display = ('id', 'seq', 'image', 'name', 'description', 'is_active', 'creation_date', 'manual_id_id',)
    list_display_links = ('id',)
    #list_filter = ('name', 'is_course')
    list_editable = ('seq', 'image', 'name', 'description', 'is_active',)
    search_fields = ('name',)
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
admin.site.register(LifeFilm, LifeFilmAdmin)

