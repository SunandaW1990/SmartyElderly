from django.shortcuts import render

# Create your views here.
def manual(request):
    context = {"input": ["Testing Manual"]}
    return render(request, "manuals/manual.html", context)
