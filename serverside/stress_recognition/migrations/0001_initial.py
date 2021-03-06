# Generated by Django 2.1 on 2019-06-29 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('predicted', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.IntegerField(choices=[(1, 'Happy'), (2, 'Sad'), (3, '3'), (4, '4'), (5, '5')])),
                ('weather', models.CharField(max_length=128)),
                ('temp_max', models.FloatField()),
                ('tmp_min', models.FloatField()),
                ('diff_tmp', models.FloatField()),
                ('humidity', models.FloatField()),
                ('predicted', models.IntegerField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stress_recognition.User')),
            ],
        ),
    ]
