from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    fans = models.IntegerField(default=0)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    desc = models.TextField(null=True, blank=True, verbose_name="描述",default='这个人很懒,什么也没有留下')
    picture = models.CharField(max_length=20,default="default.png")
    v_count = models.IntegerField(default=0)

    def getfans(id):
        return AppUser.objects.filter(id=id).values()[0]["fans"]
    def getinfo(id, info):
        return AppUser.objects.filter(id=id).values()[0][info]
    def getProfile(id):
        result = AppUser.objects.filter(id=int(id)).all().values()
        if result:
            return {
                    "username": result[0]["username"],
                    "id": result[0]["id"],
                    "picture": result[0]["picture"],
                    "fans": result[0]["fans"],
                    "follow": len(followUser.user_follow(from_user=result[0]["id"])),
                    "v_count": result[0]["v_count"],
                    "desc": str(result[0]["desc"]),
                    "is_superuser":str(result[0]["is_superuser"]),
                    "is_me":"",
                    "join":{
                        "year":result[0]["date_joined"].year,
                        "month": result[0]["date_joined"].month,
                        "day": result[0]["date_joined"].day
                    },
                    "gender":result[0]["gender"],
                }
        else:
            return 0
    def searchByName(name):
        tmp1 = AppUser.objects.filter(username=name).all().values()

        tmp2 = AppUser.objects.filter(username__contains=name).all().values()

        result1 = []
        result2 = []
        if tmp1:
            result1 = {
                    "username":tmp1[0]["username"],
                    "id":tmp1[0]["id"],
                    "picture":tmp1[0]["picture"],
                    "fans":tmp1[0]["fans"],
                    "v_count": tmp1[0]["v_count"],
                    "desc": tmp1[0]["desc"]
                }

        for item in tmp2:
            if item not in tmp1:
                result2.append({
                    "username": item["username"],
                    "id": item["id"],
                    "picture": item["picture"],
                    "fans": item["fans"],
                    "v_count":item["v_count"],
                    "desc": item["desc"]
                })
        return {
            "exactness": [result1],
            "indistinct":result2,
        }
    def addvideo(id):
        AppUser.objects.filter(id=id).update(v_count=AppUser.objects.filter(id=id).values()[0]["v_count"]+1)
    def delvideo(id):
        AppUser.objects.filter(id=id).update(v_count=AppUser.objects.filter(id=id).values()[0]["v_count"]-1)
class messages(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_content = models.CharField(max_length=400,null=False)
    m_user = models.IntegerField(null=False)
    m_time = models.DateTimeField(auto_now_add=True)

    def createMessage(m_content,m_user):
        messages(m_content=m_content, m_user=m_user).save()

    def delMessagesByUser(m_user):
        r = messages.objects.filter(m_user=m_user).all()
        if r:
            r.delete()
            return 1
        else:
            return 0

    def getMessagesByUser(m_user):
        r = messages.objects.filter(m_user=m_user).all().order_by('-m_time')
        if r:
            return r
        else:
            return 0
class collectVideo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    video_id = models.IntegerField(default=0)

    def collect_check(user_id, video_id):
        getAllCollect = collectVideo.objects.filter(user_id=user_id,video_id=video_id).all()
        if(getAllCollect):
            return 1
        else:
            return 0

    def collect(user_id, video_id):
        collectVideo(user_id = user_id,video_id=video_id).save()

    def cancelCol(user_id, video_id):
        f = collectVideo.objects.filter(user_id = user_id,video_id=video_id).all()
        if f:
            f.delete()
            return 1
        else:
            return 0

    def user_collected(user_id): #获取本人收藏的所有视频
        getAllCollect = collectVideo.objects.filter(user_id=user_id).all()
        user_collect = []
        for video in getAllCollect:
            user_collect.append(video.video_id)
        return user_collect

    def delete(v_id):
        r = collectVideo.objects.filter(video_id=v_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0
class likeVideo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    video_id = models.IntegerField(default=0)

    def love_check(user_id, video_id):
        getAllLike = likeVideo.objects.filter(user_id=user_id,video_id=video_id).all()
        if(getAllLike):
            return 1
        else:
            return 0

    def love(user_id, video_id):
        likeVideo(user_id = user_id,video_id=video_id).save()

    def dislove(user_id, video_id):
        r = likeVideo.objects.filter(user_id = user_id,video_id=video_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0

    def user_liked(user_id): #获取本人喜欢的所有视频
        getAllLike = followUser.objects.filter(user_id=user_id).all()
        user_like = []
        for video in getAllLike:
            user_like.append(video.video_id)
        return user_like
    def delete(v_id):
        r = likeVideo.objects.filter(video_id=v_id).all()
        if r:
            r.delete()
            return 1
        else:
            return 0
class followUser(models.Model):
    id = models.AutoField(primary_key=True)
    follow_id = models.IntegerField(default=0)
    followed_id = models.IntegerField(default=0)

    def follow_check(from_user, to_user):
        getAllFollow = followUser.objects.filter(follow_id=from_user,followed_id=to_user).all()
        if(getAllFollow):
            return 1
        else:
            return 0

    def follow(from_user, to_user):
        followUser(follow_id =from_user,followed_id=to_user).save()

    def unfollow(from_user, to_user):
        f = followUser.objects.filter(follow_id=from_user,followed_id=to_user).all()
        if f:
            f.delete()

    def user_follow(from_user): #获取本人关注的所有人
        getAllFollow = followUser.objects.filter(follow_id=from_user).all()
        user_follows = []
        for followeder in getAllFollow:
            user_follows.append(followeder)
        return user_follows

    def user_followed(to_user): #获取这个人都被谁关注了
        getAllFollow = followUser.objects.filter(followed_id=to_user).all().values()
        user_followed = []
        for followeder in getAllFollow:
            user_followed.append(followeder.follow)
        return user_followed
