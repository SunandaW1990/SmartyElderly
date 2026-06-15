from django.contrib import admin
from .models import CarouselImage

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'seq', 'is_active', 'creation_date']
    list_editable = ['seq', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    fields = ['title', 'image', 'seq', 'is_active', 'link_url']