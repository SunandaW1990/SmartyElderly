from django.db import models

# Create your models here.
class Manual(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    name = models.CharField(max_length=50) #(chapter / self learn course name)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='manual/', verbose_name="圖片檔案")
    detail_title = models.CharField(max_length=100)
    detail_title2 = models.CharField(max_length=100)
    detail_desc = models.CharField(max_length=200)
    explanation = models.CharField(max_length=500)
    important1 = models.CharField(max_length=100)
    important2 = models.CharField(max_length=100)
    important3 = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LifeFilm(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    manual_id = models.ForeignKey(Manual, on_delete=models.DO_NOTHING)
    seq = models.IntegerField()
    image = models.ImageField(upload_to='lifefilm/', verbose_name="圖片檔案")
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#Not Use
class ManualDetail(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    lifefilm_id = models.ForeignKey(LifeFilm, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name