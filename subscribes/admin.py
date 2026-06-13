'''
from django.contrib import admin
from django import forms
from .models import Subscriber
from taggit.forms import TagWidget
from django.forms import NumberInput
from django.db import models

# Register your models here.
class SubscriberAdminForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'
        #widgets = {
        #    'services': TagWidget(attrs={
        #        "style": "width: 100px"
        #    }),
        #}

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'tel', 'receive_email', 'creation_date')
    list_display_links = ('id', 'user_id', 'tel')
    #list_filter = ('doctor', 'services')
    list_editable = ('receive_email', )
    search_fields = ('user_id', 'tel',)
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
admin.site.register(Subscriber, SubscriberAdmin)
'''