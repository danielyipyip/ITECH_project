# Generated by Django 2.1.5 on 2021-08-04 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_page_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='image',
            field=models.ImageField(blank=True, upload_to='page_images'),
        ),
    ]
