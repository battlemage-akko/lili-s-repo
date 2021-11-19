from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from barrage.models import test as barrageTable
from barrage.models import video as videosTable
from barrage.models import discuss as discussTable
from barrage.models import answer as answerTable
from barrage.models import accusation_video as accusationTable
from django.http import HttpResponse, JsonResponse
from app.models import followUser as followtable
from app.models import collectVideo as collectTable
from app.models import messages as messagesTable
from app.models import likeVideo as lovetable
from app.models import AppUser as Userdatabase
from moviepy.editor import VideoFileClip
import random,os,re

def video(request,vid):
    result = videosTable.objects.filter(v_id=vid).values()
    if(len(result) == 0):
        return render(request,'notfound.html')
    result = result[0]
    tmp = []
    Allvideoslist = videosTable.objects.all().order_by("v_id").values()
    for i in Allvideoslist:
        tmp.append(i)
    if((tmp.index(result))+1 == len(tmp)):
        nextvideo = Allvideoslist[0]
    else:
        nextvideo = Allvideoslist[(tmp.index(result))+1]

    tmp.remove(result)
    tmp.remove(nextvideo)

    nextvideolist = []
    randomlist = random.sample(range(0, len(tmp)-2), 9)
    for i in randomlist:
        nextvideolist.append(tmp[i])

    tags = videosTable.objects.get(v_id=vid).v_tags
    discuss = discussTable.getDiscussByV_id(v_id=vid)
    for i in discuss:
        i["userdetail"] = {
            'username' : Userdatabase.getinfo(id=i['u_id'],info="username"),
            'picture' : Userdatabase.getinfo(id=i['u_id'],info="picture")
        }
        i["answer"] = answerTable.getAnswerByD_id(i['d_id'])
        for j in i["answer"]:
            j["userdetail"] = {
                'username': Userdatabase.getinfo(id=j['u_id'], info="username"),
                'picture': Userdatabase.getinfo(id=j['u_id'], info="picture")
            }
    data = {
        "v_id": result["v_id"],
        "v_ad": result["v_ad"],
        "v_pic": result["v_pic"],
        "v_auther": result["v_auther"],
        "v_play": result["v_play"],
        "v_title": result["v_title"],
        "v_collect": result["v_collect"],
        "v_like": result["v_like"],
        "user_id": result["user_id"],
        "fans": Userdatabase.getfans(result["user_id"]),
        "v_time": {
            "v_time_year": result["v_time"].year,
            "v_time_month": result["v_time"].month,
            "v_time_day": result["v_time"].day,
            "v_time_hour": result["v_time"].hour,
            "v_time_minute": result["v_time"].minute,
            "v_time_second": result["v_time"].second
        },
        "v_tags": tags,
        "u_pic": Userdatabase.getinfo(id=result["user_id"],info="picture"),
        "nextvideo": nextvideo,
        "nextvideolist": nextvideolist,
        "oncechance" : 1,
        "followornot" : followtable.follow_check(request.user.id,result["user_id"]),
        "loveornot": lovetable.love_check(request.user.id, result["v_id"]),
        "collectornot": collectTable.collect_check(request.user.id, result["v_id"]),
        "discuss": [item for item in discuss],
    }
    return render(request,'video.html',data)
@csrf_exempt
def loadbarrage(request):
    v_id = request.POST.get("v_id")
    barrage = []
    result = barrageTable.objects.filter(v_id=v_id).order_by('b_time').values()
    for i in result:
        barrage.append(i)
    return JsonResponse(barrage, safe=False)

@csrf_exempt
def getVideosList(request):
    return HttpResponse
    videos = []
    result = videosTable.objects.all().values()
    for i in result:
        videos.append(i)
    return JsonResponse(videos, safe=False)

@csrf_exempt
def hasbeenplayed(request):
    if(request.method == "POST"):
        v_id = request.POST.get("v_id")
        videosTable.objects.filter(v_id=v_id).update(v_play=videosTable.objects.filter(v_id=v_id).values()[0]['v_play']+1)
    return HttpResponse()

@csrf_exempt
def sendDiscussion(request):
    if(request.method=="POST"):
        v_id = request.POST.get("v_id")
        u_id = request.POST.get("u_id")
        d_content = request.POST.get("d_content")
        result = discussTable.create(u_id=u_id,v_id=v_id,d_content=d_content)
        if result:
            result = discussTable.getDiscussByD_id(d_id=result)
            result[0]["userdetail"] = {
                'username': Userdatabase.getinfo(id=result[0]['u_id'], info="username"),
                'picture': Userdatabase.getinfo(id=result[0]['u_id'], info="picture")
            }
            result[0]["answer"] = []
            return JsonResponse({
                "result": result,
                "msg": "发送成功"
            })
        else:
            return JsonResponse({
                "result": [],
                "msg": "发送失败"
            })

@csrf_exempt
def sendAnswer(request):
    if (request.method == "POST"):
        v_id = request.POST.get("v_id")
        u_id = request.POST.get("u_id")
        d_id = request.POST.get("d_id")
        answer_content = request.POST.get("answer_content")
        result = answerTable.create(u_id=u_id,v_id=v_id,d_id=d_id,answer_content=answer_content)
        if result:
            result = answerTable.getAnswerByAnswer_id(answer_id=result)[0]
            result["userdetail"] = {
                'username': Userdatabase.getinfo(id=result['u_id'], info="username"),
                'picture': Userdatabase.getinfo(id=result['u_id'], info="picture")
            }
            return JsonResponse({
                "result":result,
                "msg":"发送成功"
            })
        else:
            return JsonResponse({
                "result": [],
                "msg": "发送失败"
            })
@csrf_exempt
def save_barrage(request):
    if(request.method == 'POST'):
        b_content = request.POST.get("b_content")
        b_time = request.POST.get("b_time")
        b_auther = request.POST.get("b_auther")
        b_mode = request.POST.get("b_mode")
        v_id = request.POST.get("v_id")
        print(b_content,b_time,b_auther,v_id)
        result = barrageTable(b_content=b_content,b_time=b_time,b_auther=b_auther,v_id=v_id,b_mode=b_mode)
        result.save()
        return HttpResponse("上传弹幕成功")
    else:
        return HttpResponse("上传弹幕失败")

@csrf_exempt
def getmorenewvideo(request):
    result = videosTable.objects.all().order_by('-v_id').values()
    fromtag = int(request.POST.get("count"))
    totag = fromtag + 10
    newvideos = []
    if (totag > len(result)):
        totag = len(result)
    for i in result[fromtag:totag]:
        i["v_time"] = i["v_time"].strftime('%Y-%m-%d %H:%M:%S')
        newvideos.append(i)
    return JsonResponse(newvideos, safe=False)

@csrf_exempt
def getMyVideo(request):
    if(request.method == "POST"):
        count = int(request.POST.get("count"))
        u_id = request.POST.get("user_id")
        result = []
        for i in videosTable.getvideosbyid(user_id=u_id,choose="time"):
            result.append(i)
        return JsonResponse(result, safe=False)

@csrf_exempt
def getMoreCollectVideo(request):
    if(request.method == "POST"):
        user_id = request.POST.get("user_id")
        count = request.POST.get("count")
        print(user_id,count)
    return HttpResponse()

@csrf_exempt
def save_video(request):
    if(request.method == "POST"):
        video_title = request.POST.get("video_title")
        video_pic = request.FILES.get("video_pic")
        video_file = request.FILES.get("video_file")
        username = request.POST.get("username")
        user_id = request.POST.get("user_id")
        tags = request.POST.get("tags")
        tmp = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+","",tags)
        if(tmp==""):
            tags = "None"
        finish_save(video_title, video_pic, video_file,username,user_id,tags)
    return HttpResponse("上传完成")

def finish_save(video_title,video_pic,video_file,username,user_id,tags):
    video_title_tmp = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+","",video_title)

    video_pic_save_path = 'static/videos/videopic/' +  video_title_tmp + '.jpg'
    with open(video_pic_save_path, 'wb+') as f:
        f.write(video_pic.read())
    print(video_pic.name, "done")

    video_file_save_path = 'static/videos/' +  video_title_tmp + '.mp4'
    with open(video_file_save_path, 'wb+') as f:
        f.write(video_file.read())
    print(video_file.name, "done")
    time = round(VideoFileClip(video_file_save_path).duration)

    result = videosTable(v_ad=video_title_tmp + '.mp4',v_pic=video_title_tmp + '.jpg',v_auther=username,user_id=user_id,v_title=video_title,v_like=0,v_play=0,v_collect=0,v_duaring=time,v_tags=tags)
    result.save()

    messagesTable.createMessage(m_content="您成功上传了《"+video_title+"》", m_user=user_id)
    Userdatabase.addvideo(user_id)
    return HttpResponse("保存完毕")

@csrf_exempt
def del_Discussion(request):
    if (request.method == "POST"):
        d_id = request.POST.get("d_id")
        result = discussTable.delByD_id(d_id=d_id)
        if result:
            answerTable.delByD_id(d_id=d_id)
            return JsonResponse({
                "msg":"删除评论成功",
                "code": 1
            })
        else :
            return JsonResponse({
                "msg": "删除失败",
                "code": 0
            })
@csrf_exempt
def del_video(request):
    if(request.method == "POST"):
        v_id = request.POST.get("v_id")
        v = videosTable.objects.get(v_id=v_id)
        if v:
            v_title = v.v_title
            user_id = v.user_id
            v_pic = 'static/videos/videopic/' + v.v_pic
            v_ad = 'static/videos/' + v.v_ad

            if os.path.exists(v_ad) or os.path.exists(v_pic):

                os.remove(v_pic)
                os.remove(v_ad)

                v_result = videosTable.delect(v_id)
                b_result = barrageTable.delect(v_id)
                l_result = lovetable.delete(v_id)
                c_result = collectTable.delete(v_id)
                print([v_result,b_result,l_result,c_result])
                clearacc = accusationTable.delectAll(v_id=v_id)
                Userdatabase.delvideo(user_id)
                discussTable.delByV_id(v_id=v_id)
                answerTable.delByV_id(v_id=v_id)
                messagesTable.createMessage(m_content="成功删除视频《"+v_title+"》与视频弹幕,视频id(v_id)为"+v_id,m_user=user_id)
            else:
                messagesTable.createMessage(m_content="删除视频《" + v_title + "》失败",
                                            m_user=user_id)
    return HttpResponse("done")

@csrf_exempt
def report(request):
    if(request.method == "POST"):
        v_id = request.POST.get('v_id')
        v = videosTable.objects.get(v_id=v_id)
        v_title = v.v_title
        u_id = request.POST.get('u_id')
        a_reason = request.POST.get('a_reason')
        result = accusationTable.create(v_id=v_id,u_id=u_id,a_reason=a_reason)
        if(result["code"]==1):
            messagesTable.createMessage(m_content="您成功举报了《"+v_title+"》,请耐心等待管理员审核。感谢您的反馈！",m_user=u_id)
        return JsonResponse(result)

@csrf_exempt
def getAllVideoAccusation(request):
    Accusationdata = {}
    for i in accusationTable.objects.all():
        Accusationdata[i.a_id] = {
            "a_id": i.a_id,
            "v_id": i.v_id,
            "v_title": videosTable.objects.get(v_id=i.v_id).v_title,
            "u_id": i.u_id,
            "u_name": Userdatabase.objects.get(id=i.u_id).username,
            "a_reason": i.a_reason,
            "a_time": i.a_time,
        }
    print(Accusationdata)
    return JsonResponse(Accusationdata)

@csrf_exempt
def rejectVideoAccusation(request):
    if(request.method == "POST"):
        a_id = request.POST.get("a_id")
        v = videosTable.objects.get(v_id=accusationTable.objects.get(a_id=a_id).v_id)
        u = Userdatabase.objects.get(id=accusationTable.objects.get(a_id=a_id).u_id)
        accusationTable.delete(a_id=a_id)
        messagesTable.createMessage(m_content="您对《" + v.v_title + "》的举报已被驳回，如有疑问请联系管理员", m_user=u.id)
    return HttpResponse()