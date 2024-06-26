# Generated by Django 5.1a1 on 2024-06-26 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='line',
            name='stops',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='line',
        ),
        migrations.AddField(
            model_name='line',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stop',
            name='line',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='stops', to='schedule.line'),
            preserve_default=False,
        ),
    ]
