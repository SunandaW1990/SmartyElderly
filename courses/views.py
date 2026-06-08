from django.shortcuts import render

# Create your views here.
def course(request):
    context = {"input": ["Testing Course"]}
    return render(request, "courses/course.html", context)
