from django.db import models
from subscribes.models import Subscriber
from .choices import district_choices

# Create your models here.
class Course(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    comm_date = models.DateTimeField(auto_now_add=True)
    district = models.CharField(max_length=50, choices=district_choices.items(),default="")
    fee = models.IntegerField()
    topic = models.CharField(max_length=50)
    course_url = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    poster_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    subscriber_id = models.ForeignKey(Subscriber, on_delete=models.DO_NOTHING)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

