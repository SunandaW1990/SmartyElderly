from django.db import models
from django.conf import settings
#from subscribes.models import Subscriber
from .choices import district_choices, category_choices, fee_choices

# ========== 將字典轉換為 Django 可用的 choices 格式 ==========
DISTRICT_CHOICES = list(district_choices.items()) if isinstance(district_choices, dict) else district_choices
CATEGORY_CHOICES = list(category_choices.items()) if isinstance(category_choices, dict) else category_choices
FEE_CHOICES = list(fee_choices.items()) if isinstance(fee_choices, dict) else fee_choices

# Create your models here.
class Course(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    comm_date = models.DateTimeField(auto_now_add=True)


    # 使用 DISTRICT_CHOICES（已轉換）
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, default="")
    #district = models.CharField(max_length=50, choices=district_choices.items(),default="")


    # 如果您要儲存「金額」，保持 IntegerField，但不使用 fee_choices
    fee = models.IntegerField(help_text="課程費用（港幣），0 表示免費")
    #fee = models.IntegerField()


    # 使用 CATEGORY_CHOICES（已轉換）
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="手機班")
    #category = models.CharField(max_length=50)

    course_url = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    poster_img = models.ImageField(upload_to='courses/', verbose_name="圖片檔案")
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    id = models.BigAutoField(primary_key=True)	# AutoIncrementID

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('active', '已報名'), ('cancelled', '已取消')],
        default='active'
    )

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"