# Generated by Django 2.1 on 2019-06-29 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stress_recognition', '0005_auto_20190629_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media')),
            ],
        ),
    ]
