# Generated by Django 3.2.13 on 2022-07-17 12:55

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0009_auto_20220715_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='e2etestactionmodel',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='e2etestparamsmodel',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 17, 12, 54, 59, 756599)),
        ),
    ]
