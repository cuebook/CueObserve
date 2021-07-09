# Generated by Django 3.2.1 on 2021-07-09 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0016_auto_20210625_0638'),
        ('anomaly', '0006_auto_20210708_0425'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('cronSchedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.crontabschedule')),
            ],
        ),
    ]
