from django.db import models
from django.conf import settings

# Create your models here.
class Subscriber(models.Model):
    id = models.BigAutoField(primary_key=True)	#AutoIncrementID, {{user.id}} (Refer to 20260520.txt)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    tel = models.CharField(max_length=20)
    birth_year = models.CharField(max_length=10)
    birth_mth = models.CharField(max_length=10)
    contact_method = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)

