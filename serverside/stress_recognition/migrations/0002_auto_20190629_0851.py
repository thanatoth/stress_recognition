# Generated by Django 2.1 on 2019-06-29 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stress_recognition', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercondition',
            old_name='tmp_min',
            new_name='temp_min',
        ),
    ]
