
from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    fans = models.IntegerField(default=0)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    desc = models.TextField(null=True, blank=True, verbose_name="描述")
    picture = models.CharField(max_length=20,default="default.png")

    def getfans(id):
        return AppUser.objects.filter(id=id).values()[0]["fans"]

# class followUser(models.Model):
#     id = models.AutoField(primary_key=True)
#     follow_id = models.IntegerField(default=0)
#     followed_id = models.IntegerField(default=0)
#
#     def follow_check(from_user, to_user):
#         getAllFollow = followUser.objects.filter(follow_id=from_user,followed_id=to_user).all()
#         if(getAllFollow):
#             return 1
#         else:
#             return 0
#
#     def follow(from_user, to_user):
#         followUser(follow_id =from_user,followed_id=to_user).save()
#
#     def unfollow(from_user, to_user):
#         f = followUser.objects.filter(follow_id=from_user,followed_id=to_user).all()
#         if f:
#             f.delete()
#
#     def user_followed(from_user): #获取本人关注的所有人
#         getAllFollow = followUser.objects.filter(follow_id=from_user).all()
#         user_follow = []
#         for followeder in getAllFollow:
#             user_follow.append(followeder.followed)
#         return user_follow
#
#     def user_followed(to_user): #获取这个人都被谁关注了
#         getAllFollow = followUser.objects.filter(followed_id=to_user).all()
#         user_followed = []
#         for followeder in getAllFollow:
#             user_followed.append(followeder.follow)
#         return user_followed
