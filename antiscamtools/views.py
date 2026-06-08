from django.shortcuts import render

# Create your views here.
def antiscamtool(request):
    context = {"input": ["Testing AntiScamTool"]}
    return render(request, "antiscamtools/antiscamtool.html", context)
