# Generated by Django 3.2.1 on 2021-07-29 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anomaly', '0013_anomaly_latestrun'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectionRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anomalyDefinition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='anomaly.anomalydefinition')),
            ],
        ),
        migrations.CreateModel(
            name='DetectionRuleParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DetectionRuleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DetectionRuleParamValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('detectionRule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anomaly.detectionrule')),
                ('param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anomaly.detectionruleparam')),
            ],
        ),
        migrations.AddField(
            model_name='detectionruleparam',
            name='detectionRuleType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anomaly.detectionruletype'),
        ),
    ]
