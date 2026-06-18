# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class SubscribeForm(forms.Form):
    surname = forms.CharField(max_length=50, label="姓氏")
    title = forms.ChoiceField(choices=[('先生','先生'),('女士','女士'),('不便透露','不便透露')], label="稱謂")
    birth_year = forms.ChoiceField(choices=[], label="出生年份")
    birth_month = forms.ChoiceField(choices=[(str(i), f"{i}月") for i in range(1,13)], label="出生月份")
    phone = forms.CharField(max_length=20, required=False, label="電話號碼")
    email = forms.EmailField(label="電郵地址")
    password = forms.CharField(widget=forms.PasswordInput, min_length=4, label="密碼")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="確認密碼")
    notify_method = forms.ChoiceField(
        choices=[('email', '電郵通知'), ('whatsapp', 'WhatsApp通知')],
        widget=forms.RadioSelect,
        label="通知方式"
    )
    agree_terms = forms.BooleanField(label="同意接收資訊")
    agree_privacy = forms.BooleanField(label="同意私隱政策")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = [(str(y), str(y)) for y in range(2008, 1919, -1)]
        self.fields['birth_year'].choices = years
        
        for name, field in self.fields.items():
            if name not in ['notify_method', 'agree_terms', 'agree_privacy']:
                field.widget.attrs.update({'class': 'form-control'})

# accounts/forms.py - 修改 clean() 方法中的密碼檢查部分
    def clean(self):
        data = super().clean()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
    
        if not email:
            self.add_error('email', "電郵地址為必須填寫")
    
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "此電郵地址已被註冊")
    
        if phone:
            if not phone.isdigit():
                self.add_error('phone', "電話號碼必須為數字")
            elif len(phone) != 8:
                self.add_error('phone', "電話號碼必須為8位數字")
    
        pwd = data.get('password')
        confirm = data.get('confirm_password')
        if pwd and confirm and pwd != confirm:
            self.add_error('confirm_password', "密碼與確認密碼不一致")  # 改為欄位錯誤
    
        notify = data.get('notify_method')
        if notify == 'whatsapp' and not phone:
            self.add_error('notify_method', "選擇 WhatsApp 通知必須填寫電話號碼")
    
        return data

    def save(self, request=None):
        data = self.cleaned_data
        phone = data.get('phone', '').strip() or ''
        email = data.get('email', '').strip()
        
        username = email
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=data['password']
        )
        
        Profile.objects.create(
            user=user,
            surname=data['surname'],
            title=data['title'],
            phone=phone,
            birth_year=data['birth_year'],
            birth_month=data['birth_month'],
            notification_method=data['notify_method'],
        )
        
        from django.contrib.auth import login
        if request:
            login(request, user)
        
        return user