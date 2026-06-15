from django.shortcuts import render,redirect, get_object_or_404
from .models import Course, Enrollment
from django.contrib import messages
from .choices import district_choices, category_choices, fee_choices, mth_choices
from django.utils import timezone
from django.views.generic import ListView
from django.db.models import Prefetch


# Create your views here.
def courses(request):
    courses = Course.objects.order_by('-creation_date').filter(is_active=True)
    context = {"courses": courses}
    context["districts"] = district_choices.values
    context["categories"] = category_choices
    context["fees"] = fee_choices
    context["mths"] = mth_choices
    return render(request, "courses/courses.html", context)




def enroll(request):
    if request.method == "POST":
        course_id = request.POST['course_id']
        subscriber_id = request.POST['subscriber_id']

        enroll_exists = Enrollment.objects.filter(course_id=course_id, subscriber_id=subscriber_id).exists()

        if enroll_exists:
            result = 'Fail'
        else:
            enrollment = Enrollment(course_id_id=course_id, subscriber_id_id=subscriber_id, creation_date=timezone.now())
            enrollment.save()
            result = 'Success'

        courses = Course.objects.order_by('-creation_date').filter(is_active=True)
        context = {"courses": courses}
        context["districts"] = district_choices.values
        context["categories"] = category_choices
        context["fees"] = fee_choices
        context["mths"] = mth_choices
        context["result"] = [result]
        context["course_id"] = [course_id]
        enrollment = Course.objects.filter(id = course_id)
        context["enrollment"] = enrollment

        return render(request, "courses/courses.html", context)

def course(request):
    context = {"input": ["Testing Course"]}
    return render(request, "courses/course.html", context)
