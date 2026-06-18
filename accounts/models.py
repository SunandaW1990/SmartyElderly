# accounts/models.py - 完全刪除自訂 User，只保留 Profile
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """會員詳細資料 - 與內建 User 一對一關聯"""
    TITLE_CHOICES = [
        ('先生', '先生'),
        ('女士', '女士'),
        ('不便透露', '不便透露'),
    ]
    
    NOTIFY_CHOICES = [
        ('email', '電郵通知'),
        ('whatsapp', 'WhatsApp通知'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    surname = models.CharField('姓氏', max_length=50)
    title = models.CharField('稱謂', max_length=10, choices=TITLE_CHOICES)
    phone = models.CharField('電話號碼', max_length=20, blank=True)
    birth_year = models.CharField('出生年份', max_length=4, blank=True)
    birth_month = models.CharField('出生月份', max_length=2, blank=True)
    notification_method = models.CharField('通知方式', max_length=10, choices=NOTIFY_CHOICES, default='email')
    created_at = models.DateTimeField('註冊時間', auto_now_add=True)
    updated_at = models.DateTimeField('更新時間', auto_now=True)
    
    class Meta:
        verbose_name = '會員資料'
        verbose_name_plural = '會員資料列表'
    
    def __str__(self):
        return f"{self.surname}{self.title}"


class MessageToAdmin(models.Model):
    """會員發送給管理員的訊息"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='發送者')
    subject = models.CharField('主旨', max_length=200)
    content = models.TextField('訊息內容')
    is_read = models.BooleanField('管理員已讀', default=False)
    created_at = models.DateTimeField('發送時間', auto_now_add=True)
    reply = models.TextField('管理員回覆', blank=True)
    replied_at = models.DateTimeField('回覆時間', null=True, blank=True)
    
    class Meta:
        verbose_name = '會員訊息'
        verbose_name_plural = '會員訊息列表'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.subject[:30]}"