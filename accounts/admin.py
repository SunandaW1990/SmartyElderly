# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, MessageToAdmin

class ProfileInline(admin.StackedInline):
    """在 User Admin 中內嵌 Profile"""
    model = Profile
    can_delete = False
    verbose_name_plural = '會員詳細資料'

class CustomUserAdmin(UserAdmin):
    """擴充 User Admin 以顯示 Profile"""
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'get_surname', 'get_phone', 'is_staff']
    
    def get_surname(self, obj):
        return obj.profile.surname if hasattr(obj, 'profile') else '-'
    get_surname.short_description = '姓氏'
    
    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, 'profile') else '-'
    get_phone.short_description = '電話'

# 重新註冊 User（使用自訂的 CustomUserAdmin）
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'surname', 'title', 'phone', 'notification_method', 'created_at']
    search_fields = ['surname', 'phone', 'user__username']
    list_filter = ['title', 'notification_method']

@admin.register(MessageToAdmin)
class MessageToAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
    search_fields = ['subject', 'content', 'user__username']