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

class video(models.Model):
    v_id = models.AutoField(primary_key = True)
    v_title = models.CharField(max_length=50,null=False,default="default title")
    v_ad = models.CharField(max_length=50,null=False)
    v_pic = models.CharField(max_length=50)
    v_auther = models.CharField(max_length=20,null=False)
    v_play = models.IntegerField(default=0)
    v_like=models.IntegerField(default=0)
    v_collect=models.IntegerField(default=0)
    v_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = "barrage"