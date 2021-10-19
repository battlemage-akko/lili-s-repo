import json,psutil,re,datetime,socket,requests,os
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from app.models import AppUser as Userdatabase
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class CustomBackend(ModelBackend):
    # 重写authenticate,实现email与username或者更多参数
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = Userdatabase.objects.get(
                Q(username=username) | Q(email=username) )
            if user.check_password(password):
                return user
        except Exception as e:
            return None

AllUsers = [Userdatabase.objects.all()]
realIP = requests.get(url="http://members.3322.org/dyndns/getip").text
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
def video(request):
    return render(request,'video.html')

@csrf_exempt
def login_check(request):
    if (request.method == 'GET'):
        pass
    if(request.method == 'POST' and request.POST):
        username = request.POST.get("username")
        password = request.POST.get("password")
        thisuser = authenticate(username=username,password=password)
        print(thisuser,username,password)
        try:
            if thisuser is not None:
                loginthisuser(request,thisuser)
                message = {
                    "code": 1,
                    "url": "index",
                    "msg": "登录成功"
                }
                return JsonResponse(message)
            else:
                thisuser = Userdatabase.objects.filter(username=username);
                if thisuser.exists():
                    message = {
                        "code": 0,
                        "msg": "密码错误"
                    }
                    return JsonResponse(message)
                else:
                    message = {
                        "code": 0,
                        "msg": "用户不存在！"
                    }
                    return JsonResponse(message)
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
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        registercheck = Userdatabase.objects.filter(username=username).exists() | Userdatabase.objects.filter(email=email).exists()
        if registercheck:
            message = {
                "code": 0,
                "msg": "用户已注册！"
            }
            return JsonResponse(message)
        else:
            user = Userdatabase.objects.create_user(username=username, password=password, email=email)
            user.save()
            message = {
                "code": 1,
                "msg": "账号创建成功,快来登录试试吧"
            }
            AllUsers[0] = Userdatabase.objects.all()
            return JsonResponse(message)

@csrf_exempt
def serverDetail(request):
    result = {
        "CPU": "物理:" + str(psutil.cpu_count(logical=False)) + "/逻辑:" + str(psutil.cpu_count()) + "/ 利用率:" + str(
            psutil.cpu_percent(interval=1)) + "%",
        "MEM": "内存总量:" + str(round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 1)) + "G" + "/    已用:" + str(
            round(psutil.virtual_memory().used / 1024 / 1024 / 1024, 1)) + "G" + "/ 占用率:" + str(
            psutil.virtual_memory().percent) + "%",
        "DISK": "硬盘总量:" + str(round(psutil.disk_usage('/').total / 1024 / 1024 / 1024, 1)) + "G" + "/    已用:" + str(
            round(psutil.disk_usage('/').used / 1024 / 1024 / 1024, 1)) + "G",
        "TIME": str(int((datetime.datetime.now().timestamp()-psutil.boot_time())/3600)) + "小时" + str(int(((datetime.datetime.now().timestamp()-psutil.boot_time())/60)%60)) + "分钟",
        "NET": "下行:" + str(round(psutil.net_io_counters().bytes_recv/1024/1024,2))+"MB" + "/上行:" +str(round(psutil.net_io_counters().bytes_sent/1024/1024,2))+"MB",
        "IP" : "公网IP : "+realIP+" /内网IP : "+socket.gethostbyname(socket.gethostname()),
     }
    return JsonResponse(result)

@csrf_exempt
def userDetail(request):
    admin = AllUsers[0].filter(is_superuser=1)
    result = {
        "USER": len(AllUsers[0]),
        "ONLINE": "none",
        "ADMIN": len(admin),
     }
    return JsonResponse(result)

def getAllUsers(requests):
    usersdata = {}

    for i in Userdatabase.objects.all():
        usersdata[i.id] = {
            "id":i.id,
            "username":i.username,
            "email":i.email,
            "last_login":str(i.last_login),
            "is_active":i.is_active,
            "is_superuser": i.is_superuser,
        }
    print(usersdata)
    return JsonResponse(usersdata)

@csrf_exempt
def Del_user(request):
    id = request.POST.get("id")
    message = {
        "msg": ""
    }
    result = Userdatabase.objects.filter(id=id)
    if not result[0].is_superuser:
        print("这不是管理员")
        result = result.delete()
        if result:
            message = {
                "msg": "删除成功",
                "code": "1"
            }
            AllUsers[0] = Userdatabase.objects.all()
            return JsonResponse(message)
        else:
            message = {
                "msg": "删除失败,请联系管理员",
                "code": "0"
            }
            return JsonResponse(message)
    else:
        message = {
            "msg": "管理员何必为难管理员",
            "code": "0"
        }
        return JsonResponse(message)


@csrf_exempt
def rebootorshutdown(request):
    code = request.POST.get("value")
    if(code=="1"):
        os.system("reboot")
        return HttpResponse("牛逼")
    if(code=="0"):
        os.system("systemctl stop nginx")
        return HttpResponse("牛逼")
    else:
        return HttpResponse("牛逼")


