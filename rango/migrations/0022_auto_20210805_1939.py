# Generated by Django 2.1.5 on 2021-08-05 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0021_auto_20210805_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmarklist',
            name='page',
        ),
        migrations.RemoveField(
            model_name='bookmarklist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='page',
            name='bookmark',
        ),
        migrations.DeleteModel(
            name='BookmarkList',
        ),
    ]