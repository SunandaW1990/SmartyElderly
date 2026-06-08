from django.shortcuts import render

# Create your views here.
def story(request):
    context = {"input": ["Testing Story"]}
    return render(request, "stories/story.html", context)
