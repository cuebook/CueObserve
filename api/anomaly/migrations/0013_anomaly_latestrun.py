# Generated by Django 3.2.1 on 2021-07-22 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anomaly', '0012_rename_settings_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='anomaly',
            name='latestRun',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='anomaly.runstatus'),
        ),
    ]
