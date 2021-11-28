import json,psutil,re,datetime,socket,requests,os
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from app.models import AppUser as Userdatabase
from app.models import followUser as followtable
from app.models import likeVideo as lovetable
from app.models import collectVideo as collecttable
from app.models import messages as messageTable
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.clickjacking import xframe_options_exempt,xframe_options_sameorigin
from django.db.models import Q
from barrage.models import video as videosTable
from barrage.models import video_compilation as compilationTable

AllUsers = [Userdatabase.objects.all()]
# realIP = requests.get(url="http://members.3322.org/dyndns/getip").text
realIP = '0.0.0.0'
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

@login_required
def test(request):
    return render(request,'test.html')
def null(request):
    r = requests.post('http://192.168.43.114:8080/socket/chat', data = {
        'pwd':'pbkdf2_sha256$260000$A4EUuXokECx3EovbVhuawB$APUueptK/skUXjSfPawYv2XzVECo4Z40ssK17XIav88=',
        'uuid':'7',
        'user':"test"
    })
    response = HttpResponseRedirect(r.url)
    return response
def index(request):
    return render(request,'index.html',{
        "newvideolist": [],
        "hotvideolist": [],
        "collectvideolist": [],
    })
def index_back(request):
    videos = []
    Newvideos = []
    result = videosTable.objects.all().order_by('-v_id').values()
    for i in result:
        i["v_time"] = i["v_time"].strftime('%Y-%m-%d %H:%M:%S')
        videos.append(i)
    for i in range(10):
        Newvideos.append(videos[i])
    return render(request,'index back.html',{
        "newvideolist": Newvideos,
        "hotvideolist": [],

        "collectvideolist": [],
    })

def index_login(request):
    if(request.user.is_authenticated):
        return redirect('index')
    else:
        return render(request,'login.html')

def wrapper(request):
    return render(request,'wrapper.html')

@xframe_options_sameorigin
def upload_page(request):
    if request.user.is_authenticated:
        return render(request,'upload.html')
    else:
        return render(request,'notfound.html')

@csrf_exempt
def refreshmsg(request):

    result = messageTable.getMessagesByUser(request.POST.get("user_id"))
    messages = []
    if not result:
        print("empty")
        return JsonResponse({
            "msg": ["没有任何消息"],
            "msgcount": 0
        })

    for i in result.values():
        messages.append(i['m_content'])
    return JsonResponse({
        "msg":messages,
        "msgcount": len(messages)
    })

@csrf_exempt
def getNameAndPic(request):
    u_id = request.GET.get("u_id")
    return JsonResponse({
        "username":Userdatabase.getinfo(id=u_id,info="username"),
        "picture": Userdatabase.getinfo(id=u_id, info="picture"),
        "password": Userdatabase.getinfo(id=u_id, info="password"),
        "is_online": str(request.user.is_authenticated),
        "session_key":request.session.session_key,
    })

@csrf_exempt
def clearmsg(request):
    if(request.method=="POST"):
        result = messageTable.delMessagesByUser(request.POST.get("user_id"))
        if result == 1:
            return JsonResponse({
                "msg":"删除成功",
                "code":1
            })
        else:
            return JsonResponse({
                "msg": "删除失败",
                "code": 0
            })
@csrf_exempt
def java_checkAuther(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    id = request.GET.get("id")
    print(username,password,id)
    return HttpResponse("true")
@csrf_exempt
def login_check(request):
    if (request.method == 'GET'):
        pass
    if(request.method == 'POST' and request.POST):
        username = request.POST.get("username")
        password = request.POST.get("password")
        thisuser = authenticate(username=username,password=password)
        #print(thisuser,username,password)
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
    return HttpResponse("done")

def profile(request):
    user_id = request.GET.get("user")
    is_login =  request.user.is_authenticated

    if not user_id:
        if is_login:
            userdetail = Userdatabase.getProfile(request.user.id)
            userdetail["is_me"] = "True"
            return render(request, 'profile.html', {
                "profile_detail":userdetail,
                "followornot": 1,
                "collectvideolist": []
            })
        else:
            return index_login(request)
    else:
        if user_id=="me":
            userdetail = Userdatabase.getProfile(request.user.id)
            userdetail["is_me"] = "True"
            return render(request, 'profile.html', {
                "profile_detail": userdetail,
                "followornot": 1,
                "collectvideolist": []
            })
        else:
            if user_id.isdigit():
                userdetail = Userdatabase.getProfile(user_id)
                if userdetail:
                    userdetail["is_me"] = str(request.user.id == userdetail["id"])
                    return render(request, 'profile.html', {
                        "profile_detail": userdetail,
                        "followornot": followtable.follow_check(request.user.id,user_id),
                        "collectvideolist": []
                    })
                else :
                    return render(request, "notfound.html")
            else:
                return index_login(request)

def search_page(request):
    q = request.GET.get("q")
    q = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+","",q)
    result = search(q,0)
    print(q)
    if(result['user']['exactness'][0]):
        result['user']['exactness'][0]['videos'] = videosTable.getvideosbyid(user_id=result['user']['exactness'][0]['id'],choose='time')[0:5]
    else:
        result['user']['exactness'] = []
    return render(request,'search.html',{
        "result":result
    })

def search(q,count):
    queen = []
    searchByTitle = videosTable.searchByTitle(q)
    searchByTag = videosTable.searchByTag(q)
    searchByType = videosTable.searchByType(q)
    searchByAuther = videosTable.searchByAuther(q)

    for item in searchByTitle['exactness']:
        # if (len(queen) > (count+5)):
        #     break
        queen.append(item)
    for item in searchByTitle['indistinct']:
        # if (len(queen) > (count+5)):
        #     break
        if item not in queen:
            queen.append(item)
    for item in searchByType:
        # if (len(queen) > (count+5)):
        #     break
        if item not in queen:
            queen.append(item)
    for item in searchByTag:
        # if (len(queen) > (count+5)):
        #     break
        if item not in queen:
            queen.append(item)
    for item in searchByAuther:
        # if (len(queen) > (count+5)):
        #     break
        if item not in queen:
            queen.append(item)
    for item in queen:
        if item["is_collection"]:
            item["collection_count"] = compilationTable.getNumberByV_id(item['v_id'])
        item["is_collection"] = str(item["is_collection"])
    result = {
        "user": Userdatabase.searchByName(q),
        "queen": queen,
    }
    return result

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
    #print(usersdata)
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

@csrf_exempt
def follow(request):
    if(request.method=="POST"):
        follow_id = request.POST.get("follow_id")
        followed_id = request.POST.get("followed_id")
        msg = {
            "msg":"",
            "code": None
        }
        if(followed_id==follow_id):
            msg = {
                "msg": "自己关注自己？？？",
                "code": 0
            }
            return JsonResponse(msg)
        result = followtable.follow_check(from_user=follow_id,to_user=followed_id)
        if(result == 1):
            followtable.unfollow(follow_id,followed_id)
            Userdatabase.objects.filter(id=followed_id).update(
                fans=Userdatabase.objects.filter(id=followed_id).values()[0]['fans'] - 1)
            msg = {
                "msg": "取消成功",
                "code": 2
            }
            return JsonResponse(msg)
        elif(result == 0):
            followtable.follow(follow_id, followed_id)
            Userdatabase.objects.filter(id=followed_id).update(
                fans=Userdatabase.objects.filter(id=followed_id).values()[0]['fans'] + 1)
            msg = {
                "msg": "关注成功",
                "code": 1
            }
            return JsonResponse(msg)
        else:
            msg = {
                "msg": "什么玩意？？",
                "code": 9
            }
            return JsonResponse(msg)
@csrf_exempt
def love(request):
    if(request.method=="POST"):
        user_id = request.POST.get("user_id")
        video_id = request.POST.get("video_id")
        status = int(request.POST.get("status"))
        print(status,user_id,video_id)
        msg = {
            "msg":"",
            "code": None
        }
        if(status == 0):
            lovetable.love(user_id=user_id,video_id=video_id)
            videosTable.objects.filter(v_id=video_id).update(
                v_like=videosTable.objects.filter(v_id=video_id).values()[0]['v_like'] + 1)
            msg = {
                "msg": "喜欢",
                "code": 1
            }
            return JsonResponse(msg)
        elif (status == 1):
            result = lovetable.dislove(user_id=user_id,video_id=video_id)
            if(result):
                videosTable.objects.filter(v_id=video_id).update(
                    v_like=videosTable.objects.filter(v_id=video_id).values()[0]['v_like'] - 1)
                msg = {
                    "msg": "取消喜欢",
                    "code": 0
                }
                return JsonResponse(msg)
            else:
                msg = {
                    "msg": "取消失败",
                }
                return JsonResponse(msg)
        else:
            msg = {
                "msg": "什么玩意",
            }
            return JsonResponse(msg)

@csrf_exempt
def collect(request):
    if(request.method=="POST"):
        user_id = request.POST.get("user_id")
        video_id = request.POST.get("video_id")
        status = int(request.POST.get("status"))
        print(status,user_id,video_id)
        msg = {
            "msg":"",
            "code": None
        }
        if (status == 0):
            collecttable.collect(user_id=user_id, video_id=video_id)
            videosTable.objects.filter(v_id=video_id).update(
                v_collect=videosTable.objects.filter(v_id=video_id).values()[0]['v_collect'] + 1)
            msg = {
                "msg": "加入收藏",
                "code": 1
            }
            return JsonResponse(msg)
        elif (status == 1):
            result = collecttable.cancelCol(user_id=user_id, video_id=video_id)
            if (result):
                videosTable.objects.filter(v_id=video_id).update(
                    v_collect=videosTable.objects.filter(v_id=video_id).values()[0]['v_collect'] - 1)
                msg = {
                    "msg": "取消收藏",
                    "code": 0
                }
                return JsonResponse(msg)
            else:
                msg = {
                    "msg": "取消失败",
                }
                return JsonResponse(msg)
        else:
            msg = {
                "msg": "什么玩意",
            }
            return JsonResponse(msg)

@login_required
def setting(request):
    return render(request,"setting.html")




