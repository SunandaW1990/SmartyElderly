# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from .forms import SubscribeForm
from .models import Profile, MessageToAdmin
from courses.models import Enrollment, Course  # 改為使用 Enrollment 和 Course
import json


def subscribe(request):
    """會員訂閱/註冊視圖"""
    # 已登入使用者直接跳轉儀表板
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            user = form.save(request=request)
            messages.success(request, f"🎉 歡迎 {user.profile.surname}{user.profile.title} 加入耆醒老友記！")
            return redirect('welcome')
        else:
            # 顯示表單錯誤
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields.get(field, field).label}: {error}")
    else:
        form = SubscribeForm()
    
    return render(request, 'accounts/subscribe.html', {'form': form})


@login_required
def dashboard(request):
    """會員儀表板 - 使用 Enrollment 模型"""
    # 獲取使用者已報名（狀態為 active）的課程
    user_enrollments = Enrollment.objects.filter(
        user=request.user, 
        status='active'
    ).select_related('course')
    
    return render(request, 'dashboard.html', {
        'user_courses': user_enrollments,  # 模板中仍然使用 user_courses 變數
    })


# 新增：更新通知偏好
@login_required
def update_notification(request):
    if request.method == 'POST':
        profile = request.user.profile
        whatsapp = request.POST.get('notify_whatsapp')
        email_notify = request.POST.get('notify_email')
        
        # 設定通知方式
        if whatsapp and email_notify:
            profile.notification_method = 'both'
        elif whatsapp:
            profile.notification_method = 'whatsapp'
        elif email_notify:
            profile.notification_method = 'email'
        else:
            profile.notification_method = 'email'
        
        # 更新電話與電郵
        profile.phone = request.POST.get('phone', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        
        profile.save()
        request.user.save()
        messages.success(request, '✅ 通知偏好已更新')
    else:
        messages.error(request, '無效的請求')
    return redirect('accounts:dashboard')


# 新增：更新個人資料（姓氏、稱謂、密碼）
@login_required
def update_profile(request):
    if request.method == 'POST':
        profile = request.user.profile
        # 更新姓氏和稱謂
        surname = request.POST.get('surname')
        title = request.POST.get('title')
        if surname:
            profile.surname = surname
        if title:
            profile.title = title
        profile.save()

        # 更新密碼
        new_password = request.POST.get('new_password')
        if new_password:
            confirm = request.POST.get('confirm_password')
            if new_password == confirm and len(new_password) >= 4:
                request.user.set_password(new_password)
                request.user.save()
                # 保持登入狀態
                update_session_auth_hash(request, request.user)
                messages.success(request, '✅ 密碼已更新')
            else:
                messages.error(request, '❌ 密碼不一致或長度不足（最少4位）')
        else:
            messages.success(request, '✅ 個人資料已更新')
    else:
        messages.error(request, '無效的請求')
    return redirect('accounts:dashboard')


# 新增：更新課程報名狀態（AJAX）- 使用 Enrollment 模型
@login_required
def update_courses(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_course_ids = data.get('courses', [])
            
            # 將使用者所有 active 狀態的報名改為 cancelled
            Enrollment.objects.filter(
                user=request.user, 
                status='active'
            ).update(status='cancelled')
            
            # 重新建立選中的課程報名（狀態為 active）
            for course_id in selected_course_ids:
                try:
                    course = Course.objects.get(id=int(course_id))
                    # 檢查是否已有此課程的報名記錄（無論狀態）
                    enrollment, created = Enrollment.objects.get_or_create(
                        user=request.user,
                        course=course,
                        defaults={'status': 'active'}
                    )
                    # 如果已存在但狀態不是 active，更新為 active
                    if not created and enrollment.status != 'active':
                        enrollment.status = 'active'
                        enrollment.save()
                except Course.DoesNotExist:
                    pass
            
            return JsonResponse({'status': 'ok', 'message': '課程報名狀態已更新'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': '僅支援 POST 請求'}, status=405)


# 新增：發送留言給管理員
@login_required
def send_message(request):
    if request.method == 'POST':
        category = request.POST.get('category', '')
        content = request.POST.get('content', '').strip()
        if content:
            MessageToAdmin.objects.create(
                user=request.user,
                subject=f"使用者留言 - {category}",
                content=content
            )
            messages.success(request, '✅ 留言已送出，感謝您的意見！')
        else:
            messages.error(request, '❌ 請輸入留言內容')
    else:
        messages.error(request, '無效的請求')
    return redirect('accounts:dashboard')