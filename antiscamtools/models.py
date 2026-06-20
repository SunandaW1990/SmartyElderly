from django.db import models

# Create your models here.
class AntiScamTool(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    top1_contact = models.CharField(max_length=50)
    top1_description = models.CharField(max_length=50)
    top2_contact = models.CharField(max_length=50)
    top2_description = models.CharField(max_length=50)
    top3_contact = models.CharField(max_length=50)
    top3_description = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.top1_contact

class UsefulContact(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    tool_id = models.ForeignKey(AntiScamTool, on_delete=models.DO_NOTHING)
    institute = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.institute


class ScamScript(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    topic = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    realcase = models.CharField(max_length=50)
    img_s1 = models.ImageField(upload_to='antiscamtools/', verbose_name="情景一圖片")
    img_s2 = models.ImageField(upload_to='antiscamtools/', verbose_name="情景二檔案")
    img_s3 = models.ImageField(upload_to='antiscamtools/', verbose_name="情景三檔案")
    img_s4 = models.ImageField(upload_to='antiscamtools/', verbose_name="情景四檔案")
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

class AntiScamApp(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    app_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    ios_url = models.CharField(max_length=100)
    android_url = models.CharField(max_length=100)
    huawei_url = models.CharField(max_length=100)
    qr_code = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.app_name
