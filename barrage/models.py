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
    v_time = models.DateTimeField(auto_now_add=True)
    v_duaring = models.IntegerField(default=0)
    v_tags = models.CharField(max_length=1000,null=True,default="None")
    class Meta:
        app_label = "barrage"

    def getvideosbyid(user_id):
        videos = video.objects.filter(user_id=user_id).all()
        return videos

    def delect(v_id):
        v = video.objects.filter(v_id=v_id).all()
        if v:
            v.delete()
            return 1
        else:
            return 0

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

    def delect(a_id):
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