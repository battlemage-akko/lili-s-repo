# Generated by Django 3.2.7 on 2021-10-22 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barrage', '0005_test_v_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='v_collect',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='v_like',
            field=models.IntegerField(default=0),
        ),
    ]
