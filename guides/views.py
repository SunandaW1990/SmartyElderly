from django.shortcuts import render

# Create your views here.
def guide(request):
    context = {"input": ["Testing Guide"]}
    return render(request, "guides/guide.html", context)
