from django.db import models

# Create your models here.
class test(models.Model):
    b_id = models.AutoField(primary_key = True)
    b_time = models.IntegerField()
    b_content = models.TextField()
    b_auther = models.CharField(max_length=20)
    b_color = models.CharField(max_length=20,default="black")
    class Meta:
        app_label = "barrage"
