import json
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import AppUser as Userdatabase
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from myproject import urls

class CustomBackend(ModelBackend):
    # 重写authenticate,实现email与username或者更多参数
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = Userdatabase.objects.get(
                Q(username=username) | Q(email=username) )
            # if user.check_password(password):
            return user
        except Exception as e:
            return None

@login_required
def test(request):
    return render(request,'test.html')
def index(request):
    return render(request,'index.html')
def index_login(request):
    if(request.user.is_authenticated):
        return render(request, 'index.html')
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
        thisuser = authenticate(request,username=username,password=password)
        try:
            if thisuser:
                loginthisuser(request,thisuser)
                return redirect("index")
            else:
                thisuser = authenticate(request,username=username, password=username)
                if thisuser:
                    loginthisuser(request, thisuser)
                    return redirect("index")
                else:
                    return HttpResponse("不存在用户")
        except AttributeError:
            return HttpResponse("出错了")

        return redirect("login")
def loginthisuser(request,user):
    login(request,user)

def logoutthisuser(request):
    logout(request)
    return redirect("index")
@csrf_exempt
def register(request):
    if (request.method == 'GET'):
        pass
    if request.method == 'POST' and request.POST:
        username = request.POST.get("sign_up_Username")
        email = request.POST.get("sign_up_Email")
        password = request.POST.get("sign_up_Password")
        registercheck = Userdatabase.objects.filter(username=username)
        print(username,email,password)

        if registercheck:
            message = {
                "msg": "用户存在！"
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
