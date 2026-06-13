'''
from django.contrib import admin
from django import forms
from .models import GuideScenario, GuideQuestion
from taggit.forms import TagWidget
from django.forms import NumberInput
from django.db import models

# Register your models here.
class GuideScenarioAdminForm(forms.ModelForm):
    class Meta:
        model = GuideScenario
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class GuideScenarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'creation_date')
    list_display_links = ('id', 'name')
    list_filter = ('name')
    list_editable = ('is_active', )
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
    
class GuideQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = GuideQuestion
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class GuideQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'scenario_id', 'question', 'answer', 'is_active', 'creation_date')
    list_display_links = ('id', 'scenario_id', 'question')
    #list_filter = ('question')
    list_editable = ('is_active', )
    search_fields = ('question',)
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
    
admin.site.register(GuideScenario, GuideScenarioAdmin)
admin.site.register(GuideQuestion, GuideQuestionAdmin)
'''