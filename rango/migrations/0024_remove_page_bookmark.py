# Generated by Django 2.1.5 on 2021-08-05 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0023_page_bookmark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='bookmark',
        ),
    ]
