# Generated by Django 2.1 on 2019-06-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stress_recognition', '0003_auto_20190629_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercondition',
            name='expression',
            field=models.CharField(max_length=128),
        ),
    ]
