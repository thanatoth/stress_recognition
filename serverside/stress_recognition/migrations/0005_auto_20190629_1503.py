# Generated by Django 2.1 on 2019-06-29 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stress_recognition', '0004_auto_20190629_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercondition',
            name='predicted',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]
