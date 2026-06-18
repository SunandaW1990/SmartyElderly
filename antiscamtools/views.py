from django.shortcuts import render
from .models import AntiScamTool, UsefulContact, ScamScript
from django.utils import timezone

# Create your views here.
def tools(request):
    antiscamtools = AntiScamTool.objects.order_by('-creation_date').filter(is_active=True)
    usefulcontacts = UsefulContact.objects.order_by('-creation_date').filter(is_active=True)
    scamscripts = ScamScript.objects.order_by('-creation_date').filter(is_active=True)
    context = {"scamscripts": scamscripts, "antiscamtools": antiscamtools, "usefulcontacts": usefulcontacts}
    return render(request, "antiscamtools/tools.html", context)

def antiscamtool(request):
    context = {"input": ["Testing AntiScamTool"]}
    return render(request, "antiscamtools/antiscamtool.html", context)
