# Generated by Django 2.1 on 2019-06-29 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stress_recognition', '0007_auto_20190629_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='faces'),
        ),
    ]