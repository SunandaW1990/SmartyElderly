from django.db import models
from subscribes.models import Subscriber

# Create your models here.
class Story(models.Model):
    id = models.BigAutoField(primary_key=True)	#AutoIncrementID
    subscriber_id = models.ForeignKey(Subscriber, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    category = models.CharField(max_length=50)
    speech_url = models.CharField(max_length=100)
    is_published = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
