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