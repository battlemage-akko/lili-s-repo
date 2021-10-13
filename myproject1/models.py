from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone


class User(models.Model):
    GENDER_CHOICE = (('male', '男'),
                     ('female', '女'),
                     ('unknown', '保密'),)
    user_id = models.IntegerField(primary_key=True, auto_created=True, unique=True)
    user_name = models.CharField('用户名', max_length=20)
    user_password = models.CharField('密码', max_length=20)
    hash_password = models.CharField('哈希密码', max_length=128, null=True, blank=True)
    user_gender = models.CharField('性别', choices=GENDER_CHOICE, max_length=9)
    user_email = models.CharField('邮箱', max_length=100, unique=True)
    # last_login_time =
    # is_active
    # user_phone =
    register_time = models.DateTimeField('注册日期', default=timezone.now)
    

    class Meta:
        db_table = 'user'
    def __str__(self):
        return '<class User>{}'.format(self.user_name)

