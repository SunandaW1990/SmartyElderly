from django.shortcuts import render

# Create your views here.
def subscribe(request):
    context = {"input": ["Testing Subscribe"]}
    return render(request, "subscribes/subscribe.html", context)
