from django.db import models

# Create your models here.
class Subscriber(models.Model):
    id = models.BigAutoField(primary_key=True)	#AutoIncrementID, {{user.id}} (Refer to 20260520.txt)
    receive_email = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

