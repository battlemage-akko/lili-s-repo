# Generated by Django 3.2.7 on 2021-10-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barrage', '0006_auto_20211022_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='b_size',
            field=models.IntegerField(default=15),
        ),
    ]
