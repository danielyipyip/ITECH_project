# Generated by Django 2.1.5 on 2021-08-06 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0028_bookmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likecount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
