# Generated by Django 3.2.13 on 2022-07-15 19:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0008_auto_20220715_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e2etestactionmodel',
            name='css_selector_click',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='e2etestparamsmodel',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 15, 19, 42, 56, 173534)),
        ),
    ]
