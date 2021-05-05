from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.
from utils.tencent import sms
from django.conf import settings


def send_sms(request):
    """发送短信
    ?tpl=login => 947221
    ?tpl=register => 947220
    """

    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模板不存在')

    code = random.randrange(1000, 9999)
    res = sms.send_sms_single('135336404', 947220, [code, ])
    print(res)

    if res['result'] == 0:
        return HttpResponse('发送成功')
    else:
        return HttpResponse(res['errmsg'])


# 实现注册的功能：
from django import forms
from app01 import models
from django.core.validators import RegexValidator

# 创建用户注册表单


class RegisterModelForm(forms.ModelForm):
    username = forms.CharField(label='用户名')
    email = forms.EmailField(label='邮箱',
                             widget=forms.TextInput(attrs={'placeholder': '请输入邮箱'}))    # 实现重写models中的同名字段
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'),],
                                   widget=forms.TextInput(attrs={'placeholder': '请输入手机号码'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'}))    # 显示上修改为密文
    confirm_password = forms.CharField(label='重复密码',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    code = forms.CharField(label='验证码',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入验证码'}))

    # 重写ModelForm的__init__方法来定义class=form-control来改变默认的表单样式，定义placeholder来代替每个字段都要写attrs的placeholder
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)

    class Meta:
        model = models.UserInfo
        # fields = "__all__"      # 这里__all__会使字段显示的顺序按照Models文件中定义的字段顺序->ModelForm中自定义的字段顺序来展示
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']  # 显式定义页面中字段的显示顺序


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
# 注：模板中的field.label使用的就是models中的field字段中的verbose_name

#