# Generated by Django 3.2.7 on 2021-10-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barrage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='b_color',
            field=models.CharField(default='black', max_length=20),
        ),
    ]
