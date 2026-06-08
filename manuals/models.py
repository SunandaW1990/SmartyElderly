from django.db import models

# Create your models here.
class Manual(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    name = models.CharField(max_length=50) #(chapter / self learn course name)
    description = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)
    is_course = models.BooleanField(default=True)
    course_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name