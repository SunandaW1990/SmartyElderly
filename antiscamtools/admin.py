from django.contrib import admin
from django import forms
from .models import AntiScamTool, UsefulContact, ScamScript, AntiScamApp
from taggit.forms import TagWidget
from django.forms import NumberInput
from django.db import models

# Register your models here.
class AntiScamToolAdminForm(forms.ModelForm):
    class Meta:
        model = AntiScamTool
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class AntiScamToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'top1_contact', 'top1_description', 'top2_contact', 'top2_description', 
                    'top3_contact', 'top3_description', 'is_active', 'creation_date')
    list_display_links = ('id',)
    #list_filter = ('doctor', 'services')
    list_editable = ('top1_contact', 'top1_description', 'top2_contact', 'top2_description', 
                    'top3_contact', 'top3_description', 'is_active', )
    search_fields = ('top1_contact', 'top2_contact', 'top3_contact',)
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

class UsefulContactAdminForm(forms.ModelForm):
    class Meta:
        model = UsefulContact
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class UsefulContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'institute', 'contact', 'is_active', 'creation_date', 'tool_id_id')
    list_display_links = ('id', 'creation_date', 'tool_id_id')
    #list_filter = ('doctor', 'services')
    list_editable = ('institute', 'contact', 'is_active',)
    search_fields = ('institute', 'contact',)
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

class ScamScriptAdminForm(forms.ModelForm):
    class Meta:
        model = ScamScript
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class ScamScriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'description', 'realcase', 'img_s1', 'img_s2', 'img_s3', 'img_s4', 
                    'is_active', 'creation_date')
    list_display_links = ('id', 'creation_date')
    #list_filter = ('doctor', 'services')
    list_editable = ('topic', 'description', 'realcase', 'img_s1', 'img_s2', 'img_s3', 'img_s4', 'is_active',)
    search_fields = ('topic',)
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

'''
class AntiScamAppAdminForm(forms.ModelForm):
    class Meta:
        model = AntiScamApp
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class AntiScamAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_name', 'pc_url', 'apple_url', 'android_url', 'is_active', 'creation_date')
    list_display_links = ('id', 'app_name')
    #list_filter = ('doctor', 'services')
    list_editable = ('is_active', )
    search_fields = ('app_name',)
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
'''


admin.site.register(AntiScamTool, AntiScamToolAdmin)
admin.site.register(UsefulContact, UsefulContactAdmin)
admin.site.register(ScamScript, ScamScriptAdmin)
#admin.site.register(AntiScamApp, AntiScamAppAdmin)