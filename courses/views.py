from django.shortcuts import render
from .models import Course, Enrollment
from .choices import district_choices, category_choices, fee_choices, mth_choices
from django.utils import timezone


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

        enroll_exists = Enrollment.objects.filter(course_id=course_id, user_id=subscriber_id).exists()

        if enroll_exists:
            result = 'Fail'
        else:
            enrollment = Enrollment(course_id=course_id, user_id=subscriber_id, enrollment_date=timezone.now())
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
