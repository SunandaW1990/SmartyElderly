'''
from django.contrib import admin
from django import forms
from .models import Course, Enrollment
from taggit.forms import TagWidget
from django.forms import NumberInput
from django.db import models

# Register your models here.
class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'services': TagWidget(attrs={
                "style": "width: 100px"
            }),
        }

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'comm_date', 'district', 'fee', 'topic', 'course_url', 'contact', 'poster_url', 'is_active', 'creation_date')
    list_display_links = ('id', 'title', 'district', 'topic')
    #list_filter = ('doctor', 'services')
    list_editable = ('is_active', )
    search_fields = ('title', 'district', 'topic', 'topic',)
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

class EnrollmentAdminForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber_id', 'course_id', 'creation_date')
    list_display_links = ('id', 'subscriber_id', 'course_id')
    #list_filter = ('doctor', 'services')
    #list_editable = ('is_published', )
    search_fields = ('subscriber_id', 'course_id',)
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

admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
'''