# Generated by Django 2.1.5 on 2021-08-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0029_auto_20210806_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='uploader',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
