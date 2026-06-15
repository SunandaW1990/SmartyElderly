from django.shortcuts import render
from .models import CarouselImage

def index(request):
    carousel_images = CarouselImage.objects.filter(is_active=True)
    return render(request, 'index.html', {'carousel_images': carousel_images})