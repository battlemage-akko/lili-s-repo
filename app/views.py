import json
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import AppUser as Userdatabase
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from myproject import urls

@login_required
def test(request):
    return render(request,'test.html')
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')
def wrapper(request):
    return render(request,'wrapper.html')

@csrf_exempt
def login_check(request):
    if (request.method == 'GET'):
        pass
    if(request.method == 'POST' and request.POST):
        context = {
            'message': ''
        }
        username = request.POST.get("sign_in_Username")
        password = request.POST.get("sign_in_Password")
        thisuser = authenticate(username=username,password=password)
        try:
            if thisuser:
                return redirect("index")
        except AttributeError:
            return HttpResponse("出错了")

        return redirect("login")

@csrf_exempt
def register(request):
    if (request.method == 'GET'):
        pass
    if request.method == 'POST' and request.POST:
        username = request.POST.get("sign_up_Username")
        password = request.POST.get("sign_up_Password")
        email = request.POST.get("sign_up_Email")
        registercheck = Userdatabase.objects.filter(username=username)

        if registercheck:
            message = {
                "msg": "用户存在"
            }
            return render(request, "login.html", context=message)
        else:
            user = Userdatabase.objects.create_user(username=username, password=password, email=email)
            user.save()
            message = {
                "msg": "账号创建成功,快来登录试试吧"
            }
            return render(request, "login.html", context=message)
        return redirect("login")
# Create your views here.
