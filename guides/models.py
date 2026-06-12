from django.db import models

# Create your models here.
class GuideScenario(models.Model):
    id = models.BigAutoField(primary_key=True)	#AutoIncrementID
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GuideQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)	#AutoIncrementID
    scenario_id = models.ForeignKey(GuideScenario, on_delete=models.DO_NOTHING)
    question = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
