# Generated by Django 2.1 on 2019-06-30 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stress_recognition', '0009_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='date_published'),
        ),
    ]
