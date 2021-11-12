from django.db import models

# Create your models here.
class test(models.Model):
    b_id = models.AutoField(primary_key = True)
    b_time = models.IntegerField()
    b_content = models.TextField()
    b_auther = models.CharField(max_length=20,null=True)
    b_color = models.CharField(max_length=20,default="black")
    b_size = models.IntegerField(default=15)
    v_id = models.IntegerField(default=1)
    class Meta:
        app_label = "barrage"

    def delect(v_id):
        b = test.objects.filter(v_id=v_id).all()
        if b:
            b.delete()
            return 1
        else:
            return 0

class video(models.Model):
    v_id = models.AutoField(primary_key = True)
    v_title = models.CharField(max_length=50,null=False,default="default title")
    v_ad = models.CharField(max_length=50,null=False)
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
    v_note = models.CharField(max_length=1000,null=True,default="这个人很懒,什么都没有留下")
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
                "v_note": item["v_note"],
                "v_duaring": item["v_duaring"],
                "v_time": {
                    "v_time_year": item["v_time"].year,
                    "v_time_month": item["v_time"].month,
                    "v_time_day": item["v_time"].day,
                    "v_time_hour": item["v_time"].hour,
                    "v_time_minute": item["v_time"].minute,
                    "v_time_second": item["v_time"].second
                },
                "v_type": item["v_type"],
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
                "v_play": item["v_play"],
                "v_title": item["v_title"],
                "v_time": {
                    "v_time_year": item["v_time"].year,
                    "v_time_month": item["v_time"].month,
                    "v_time_day": item["v_time"].day,
                    "v_time_hour": item["v_time"].hour,
                    "v_time_minute": item["v_time"].minute,
                    "v_time_second": item["v_time"].second
                },
                "v_note": item["v_note"],
                "v_type": item["v_type"],
            })
        for item in tmp2:
            if item not in tmp:
                indistinct.append({
                    "v_id": item["v_id"],
                    "v_pic": item["v_pic"],
                    "v_auther": item["v_auther"],
                    "v_play": item["v_play"],
                    "v_title": item["v_title"],
                    "v_time": {
                        "v_time_year": item["v_time"].year,
                        "v_time_month": item["v_time"].month,
                        "v_time_day": item["v_time"].day,
                        "v_time_hour": item["v_time"].hour,
                        "v_time_minute": item["v_time"].minute,
                        "v_time_second": item["v_time"].second
                    },
                    "v_note": item["v_note"],
                    "v_type": item["v_type"],
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
                "v_play": item["v_play"],
                "v_title": item["v_title"],
                "v_time": {
                    "v_time_year": item["v_time"].year,
                    "v_time_month": item["v_time"].month,
                    "v_time_day": item["v_time"].day,
                    "v_time_hour": item["v_time"].hour,
                    "v_time_minute": item["v_time"].minute,
                    "v_time_second": item["v_time"].second
                },
                "v_note": item["v_note"],
                "v_type": item["v_type"],
            })
        return result

    def searchByAuther(user):
        tmp = video.objects.filter(v_auther=user).all().order_by("-v_time").values()
        tmp2 = video.objects.filter(v_auther__contains=user).all().order_by("-v_time").values()
        exactness = []
        indistinct = []
        for item in tmp:
            exactness.append({
                "v_id": item["v_id"],
                "v_pic": item["v_pic"],
                "v_auther": item["v_auther"],
                "v_play": item["v_play"],
                "v_title": item["v_title"],
                "v_time": {
                    "v_time_year": item["v_time"].year,
                    "v_time_month": item["v_time"].month,
                    "v_time_day": item["v_time"].day,
                    "v_time_hour": item["v_time"].hour,
                    "v_time_minute": item["v_time"].minute,
                    "v_time_second": item["v_time"].second
                },
                "v_note": item["v_note"],
                "v_type": item["v_type"],
            })
        for item in tmp2 :
            if item not in tmp:
                indistinct.append({
                    "v_id": item["v_id"],
                    "v_pic": item["v_pic"],
                    "v_auther": item["v_auther"],
                    "v_play": item["v_play"],
                    "v_title": item["v_title"],
                    "v_time": {
                        "v_time_year": item["v_time"].year,
                        "v_time_month": item["v_time"].month,
                        "v_time_day": item["v_time"].day,
                        "v_time_hour": item["v_time"].hour,
                        "v_time_minute": item["v_time"].minute,
                        "v_time_second": item["v_time"].second
                    },
                    "v_note": item["v_note"],
                    "v_type": item["v_type"],
                })
        return {
            "exactness": exactness,
            "indistinct": indistinct,
        }


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