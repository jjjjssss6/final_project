from django.http import HttpResponse

import TeacherAccount.logic
from TeacherAccount.models import AccountSystem
import json
from typing import Any
from django.contrib import auth
from examination.logic import ComplexEncoder
# Create your views here

def Login(request):
    login_req = json.loads(request.body.decode('utf_8'))
    login_resp = {}
    account_name = login_req.get('account_name')
    account_pass = login_req.get('account_pass')
    user = auth.authenticate(username=account_name, password=account_pass)
    if user:
        login_resp['err_msg'] = '登录成功'
        login_resp['ticket'] = TeacherAccount.logic.EncodeTicket(str(user.id))
        return HttpResponse(json.dumps(login_resp, cls=ComplexEncoder, ensure_ascii=False))
    else:
        login_resp['err_msg'] = '登录失败'
        return HttpResponse(json.dumps(login_resp, cls=ComplexEncoder, ensure_ascii=False))