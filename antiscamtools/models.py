from django.db import models

# Create your models here.
class AntiScamTool(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    institute = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    event = models.CharField(max_length=100) #(MUST NOT DO EVENT)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ScamScript(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    topic = models.CharField(max_length=50)
    img_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AntiScamApp(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    app_name = models.CharField(max_length=50)
    pc_url = models.CharField(max_length=100)
    apple_url = models.CharField(max_length=100)
    android_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
