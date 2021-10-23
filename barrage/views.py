from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from barrage.models import test as barrageDatabase
from barrage.models import video as videosTable
from django.http import HttpResponse, JsonResponse

# Create your views here.
def video(request,vid):
    result = videosTable.objects.filter(v_id=vid).values()
    if(len(result) == 0):
        return HttpResponse("没有这个视频")
    result = result[0]
    data = {
        "v_id": result["v_id"],
        "v_ad": result["v_ad"],
        "v_pic": result["v_pic"],
        "v_auther": result["v_auther"],
        "v_play": result["v_play"],
        "v_title": result["v_title"],
    }
    return render(request,'video.html',data)

@csrf_exempt
def loadbarrage(request):
    v_id = request.POST.get("v_id")
    barrage = []
    result = barrageDatabase.objects.filter(v_id=v_id).order_by('b_time').values()
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
    print(videos)
    return JsonResponse(videos, safe=False)

@csrf_exempt
def save_barrage(request):
    if(request.method == 'POST'):
        b_content = request.POST.get("b_content")
        b_time = request.POST.get("b_time")
        b_auther = request.POST.get("b_auther")
        v_id = request.POST.get("v_id")
        print(b_content,b_time,b_auther,v_id)
        result = barrageDatabase(b_content=b_content,b_time=b_time,b_auther=b_auther,v_id=v_id)
        result.save()
        return HttpResponse("上传弹幕成功")
    else:
        return HttpResponse("上传弹幕失败")

@csrf_exempt
def getmorehotvideo(request):
    fromtag = int(request.POST.get("count"))
    totag = fromtag + 10
    result = videosTable.objects.all().values()
    hotvideos = []
    if (totag > len(result)):
        totag = len(result)
    for i in result[fromtag:totag]:
        hotvideos.append(i)
    print(hotvideos)
    return JsonResponse(hotvideos, safe=False)

@csrf_exempt
def save_video(request):
    if(request.method == "POST"):
        video_title = request.POST.get("video_title")
        video_pic = request.FILES.get("video_pic")
        video_file = request.FILES.get("video_file")
        username = request.POST.get("username")
        print(video_file.name)
        finish_save(video_title, video_pic, video_file,username)
    return HttpResponse("上传完成")

def finish_save(video_title,video_pic,video_file,username):
    video_pic_save_path = 'static/videos/videopic/' + video_title + '.jpg'
    with open(video_pic_save_path, 'wb+') as f:
        f.write(video_pic.read())
    print(video_pic.name, "done")

    video_file_save_path = 'static/videos/' + video_title + '.mp4'
    with open(video_file_save_path, 'wb+') as f:
        f.write(video_file.read())
    print(video_file.name, "done")

    result = videosTable(v_ad=video_title + '.mp4',v_pic=video_title + '.jpg',v_auther=username,v_title=video_title,v_like=0,v_play=0,v_collect=0)
    result.save()

    return HttpResponse("保存完毕")
