# Generated by Django 3.2.7 on 2021-10-26 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_followuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='fans',
            field=models.IntegerField(default=0),
        ),
    ]
