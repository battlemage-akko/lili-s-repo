from django.db import models
from general.views import time_normalization
# Create your models here.
class test(models.Model):
    b_id = models.AutoField(primary_key = True)
    b_time = models.IntegerField()
    b_content = models.TextField()
    b_auther = models.CharField(max_length=20,null=True)
    b_color = models.CharField(max_length=20,default="black")
    b_size = models.IntegerField(default=15)
    v_id = models.IntegerField(default=1)
    vc_id = models.IntegerField(null=True)
    b_mode = models.CharField(max_length=15,default="move")
    send_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = "barrage"

    def delect(v_id):
        b = test.objects.filter(v_id=v_id).all()
        if b:
            b.delete()
            return 1
        else:
            return 0
    def getBarrageByV_id(v_id):
        return len(test.objects.filter(v_id=v_id).all().values())
class video(models.Model):
    v_id = models.AutoField(primary_key = True)
    v_title = models.CharField(max_length=50,null=False,default="default title")
    v_ad = models.CharField(max_length=50,null=True)
    v_pic = models.CharField(max_length=50)
    v_auther = models.CharField(max_length=20,null=False)
    user_id = models.IntegerField(null=False)
    v_play = models.IntegerField(default=0)
    v_like=models.IntegerField(default=0)
    v_collect=models.IntegerField(default=0)
    v_type = models.CharField(max_length=20,null=False,default="二次元")
    v_time = models.DateTimeField(auto_now_add=True)
    v_duaring = models.IntegerField(default=0)
    v_tags = models.CharField(max_length=1000,null=True,default="None")
    v_note = models.CharField(max_length=5000,null=True,default="这个人很懒,什么都没有留下！")
    v_barrage = models.IntegerField(default=0)
    is_collection =models.BooleanField(default=False)
    class Meta:
        app_label = "barrage"

    def getvideosbyid(user_id,choose):
        tmp = video.objects.filter(user_id=user_id).all().values()
        if(choose=="time"):
            tmp = video.objects.filter(user_id=user_id).all().order_by('-v_time').values()
        videos = []
        for item in tmp:
            videos.append({
                "v_id":item["v_id"],
                "v_title": item["v_title"],
                "v_pic": item["v_pic"],
                "v_play": item["v_play"],
                "v_like": item["v_like"],
                "v_collect": item["v_collect"],
                "v_note": item["v_note"].replace("\n", "<br>"),
                "v_duaring": item["v_duaring"],
                "v_time": time_normalization(item["v_time"]),
                "v_type": item["v_type"],
                "is_collection": str(item["is_collection"]),
            })
        return videos

    def delect(v_id):
        v = video.objects.filter(v_id=v_id).all()
        if v:
            v.delete()
            return 1
        else:
            return 0

    def searchByTitle(title):
        tmp = video.objects.filter(v_title=title).all().order_by("-v_time").values()
        tmp2 = video.objects.filter(v_title__contains=title).all().order_by("-v_time").values()
        exactness = []
        indistinct = []
        for item in tmp:
            exactness.append({
                "v_id": item["v_id"],
                "v_pic": item["v_pic"],
                "v_auther": item["v_auther"],
                "v_auther_id": item["user_id"],
                "v_play": item["v_play"],
                "v_title": item["v_title"],
                "v_time": time_normalization(item["v_time"]),
                "v_note": item["v_note"].replace("\n", "<br>"),
                "v_type": item["v_type"],
                "is_collection": item["is_collection"],
            })
        for item in tmp2:
            if item not in tmp:
                indistinct.append({
                    "v_id": item["v_id"],
                    "v_pic": item["v_pic"],
                    "v_auther": item["v_auther"],
                    "v_auther_id": item["user_id"],
                    "v_play": item["v_play"],
                    "v_title": item["v_title"],
                    "v_time": time_normalization(item["v_time"]),
                    "v_note": item["v_note"].replace("\n", "<br>"),
                    "v_type": item["v_type"],
                    "is_collection": item["is_collection"],
                })
        return {
            "exactness": exactness,
            "indistinct": indistinct,
        }

    def searchByTag(tag):
        tmp = video.objects.filter(v_tags__contains=tag).all().order_by("-v_time").values()
        result = []
        for item in tmp:
            result.append({
                "v_id": item["v_id"],
                "v_pic": item["v_pic"],
                "v_auther": item["v_auther"],
                "v_auther_id": item["user_id"],
                "v_play": item["v_play"],
                "v_title": item["v_title"],
                "v_time": time_normalization(item["v_time"]),
                "v_note": item["v_note"].replace("\n", "<br>"),
                "v_type": item["v_type"],
                "is_collection": item["is_collection"],
            })
        return result

    def searchByType(type):
        tmp = video.objects.filter(v_type=type).all().order_by("-v_time").values()
        result = []
        for item in tmp:
            result.append({
                "v_id": item["v_id"],
                "v_pic": item["v_pic"],
                "v_auther": item["v_auther"],
                "v_auther_id": item["user_id"],
                "v_play": item["v_play"],
                "v_title": item["v_title"],
                "v_time": time_normalization(item["v_time"]),
                "v_note": item["v_note"].replace("\n", "<br>"),
                "v_type": item["v_type"],
                "is_collection": item["is_collection"],
            })
        return result

    def searchByAuther(user):
        tmp = video.objects.filter(v_auther=user).all().order_by("-v_time").values()
        result = []
        for item in tmp:
            result.append({
                "v_id": item["v_id"],
                "v_pic": item["v_pic"],
                "v_auther": item["v_auther"],
                "v_auther_id": item["user_id"],
                "v_play": item["v_play"],
                "v_title": item["v_title"],
                "v_time": time_normalization(item["v_time"]),
                "v_note": item["v_note"].replace("\n", "<br>"),
                "v_type": item["v_type"],
                "is_collection": item["is_collection"],
            })
        return result
class video_compilation(models.Model):
    vc_id = models.AutoField(primary_key=True)
    v_id = models.IntegerField(null=False)
    vc_title = models.CharField(max_length=50, null=False, default="None")
    vc_ad = models.CharField(max_length=200, null=False)
    vc_time = models.DateTimeField(auto_now_add=True)
    vc_duaring = models.IntegerField(default=0)
    vc_barrage = models.IntegerField(default=0)
    vc_index = models.IntegerField(default=1,null=True)

    def create(v_id,vc_title,vc_ad,vc_duaring,vc_index):
        video_compilation(v_id=v_id,vc_title=vc_title,vc_ad=vc_ad,vc_duaring=vc_duaring,vc_index=vc_index).save()
        return 1
    def deleteByV_id(v_id):
        r = video_compilation.objects.filter(v_id=v_id).all()
        if r:
            r.delete()
            return 1
        else :
            return 0
    def getNumberByV_id(v_id):
        return video_compilation.objects.filter(v_id=v_id).count()

    def getVc_adsByV_id(v_id):
        tmp = video_compilation.objects.filter(v_id=v_id).order_by('vc_index').all().values()
        result = []
        for i in tmp:
            result.append(i)
        for item in result:
            item['vc_time'] = time_normalization(item['vc_time'])

        return result
    def getVc_titleByV_id(v_id):
        result = []
        for item in video_compilation.objects.filter(v_id=v_id).all().values():
            result.append(item["vc_title"])
        return result
class accusation_video(models.Model):
    a_id = models.AutoField(primary_key=True)
    v_id = models.IntegerField()
    u_id = models.IntegerField()
    a_reason = models.CharField(max_length=500,null=False)
    a_time = models.DateTimeField(auto_now_add=True)

    def delectAll(v_id):
        r = accusation_video.objects.filter(v_id=v_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0

    def delete(a_id):
        r = accusation_video.objects.filter(a_id=a_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0

    def accusation_check(u_id,v_id):
        r = accusation_video.objects.filter(u_id=u_id,v_id=v_id).all()
        if not r:
            return 1
        else :
            return 0

    def create(u_id,v_id,a_reason):
        if accusation_video.accusation_check(u_id,v_id):
            accusation_video(u_id=u_id, v_id=v_id, a_reason=a_reason).save()
            return {
                "msg":"举报成功",
                "code":1
            }
        else:
            return {
                "msg":"后台已有待处理的举报",
                "code": 0
            }
class discuss(models.Model):
    d_id = models.AutoField(primary_key=True)
    v_id = models.IntegerField()
    u_id = models.IntegerField()
    d_content = models.CharField(max_length=500,null=False)
    d_answer = models.BooleanField(default=False)
    answer_id = models.IntegerField(null=True)
    agreement = models.IntegerField(default=0)
    disagreement = models.IntegerField(default=0)
    d_time = models.DateTimeField(auto_now_add=True)
    def create(u_id,v_id,d_content):
        if not discuss(u_id=u_id, v_id=v_id, d_content=d_content).save():
            return discuss.objects.filter(u_id=u_id, v_id=v_id, d_content=d_content).values()[0][
                'd_id']
        else:
            return 0
    def delByV_id(v_id):
        r =  discuss.objects.filter(v_id=v_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0

    def delByD_id(d_id):
        r =  discuss.objects.filter(d_id=d_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0

    def getDiscussByD_id(d_id):
        tmp = discuss.objects.get(d_id=d_id)
        result = []
        if tmp:
            tmp = tmp.__dict__
            result.append({
                "u_id": tmp["u_id"],
                "d_id": tmp["d_id"],
                "d_content": tmp["d_content"],
                "agreement": tmp["agreement"],
                "disagreement": tmp["disagreement"],
                "d_time": {
                    "d_time_year": tmp["d_time"].year,
                    "d_time_month": tmp["d_time"].month,
                    "d_time_day": tmp["d_time"].day,
                    "d_time_hour": tmp["d_time"].hour,
                    "d_time_minute": tmp["d_time"].minute,
                    "d_time_second": tmp["d_time"].second
                },
            })
        return result

    def getDiscussByV_id(v_id):
        tmp = discuss.objects.filter(v_id=v_id).order_by('-d_time').all().values()
        result = []
        for item in tmp:
            result.append({
                "u_id": item["u_id"],
                "d_id": item["d_id"],
                "d_content": item["d_content"],
                "agreement": item["agreement"],
                "disagreement": item["disagreement"],
                "d_time": time_normalization(item["d_time"]),
            })
        return result
class answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    v_id = models.IntegerField()
    d_id = models.IntegerField()
    u_id = models.IntegerField()
    answer_content = models.CharField(max_length=500,null=False)
    answer_time = models.DateTimeField(auto_now_add=True)
    d_id = models.IntegerField(null=False)
    agreement = models.IntegerField(default=0)
    disagreement = models.IntegerField(default=0)
    def delByV_id(v_id):
        r =  answer.objects.filter(v_id=v_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0
    def delByD_id(d_id):
        r =  answer.objects.filter(d_id=d_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0
    def create(u_id,v_id,answer_content,d_id):
        if not answer(u_id=u_id, v_id=v_id, answer_content=answer_content, d_id=d_id).save() :
            return answer.objects.filter(u_id=u_id, v_id=v_id, answer_content=answer_content, d_id=d_id).values()[0]['answer_id']
        else :
            return 0

    def getAnswerByAnswer_id(answer_id):
        tmp = answer.objects.get(answer_id=answer_id)
        result = []

        if tmp:
            tmp = tmp.__dict__
            result.append({
                "u_id": tmp["u_id"],
                "d_id": tmp["d_id"],
                "answer_id": tmp["answer_id"],
                "answer_content": tmp["answer_content"],
                "agreement": tmp["agreement"],
                "disagreement": tmp["disagreement"],
                "answer_time": time_normalization(tmp["answer_time"]),
            })
        return result

    def getAnswerByD_id(d_id):
        tmp = answer.objects.filter(d_id=d_id).order_by('-answer_time').all().values()
        result = []
        for item in tmp:
            result.append({
                "u_id": item["u_id"],
                "d_id": item["d_id"],
                "answer_id": item["answer_id"],
                "answer_content": item["answer_content"],
                "agreement": item["agreement"],
                "disagreement": item["disagreement"],
                "answer_time": time_normalization(item["answer_time"]),
            })
        return result
