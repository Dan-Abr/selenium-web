# Generated by Django 3.2.13 on 2022-08-16 13:03

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0018_auto_20220815_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e2etestparamsmodel',
            name='launches_per_day',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1440)]),
        ),
        migrations.AlterField(
            model_name='e2etestparamsmodel',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 16, 13, 3, 1, 238209)),
        ),
    ]
