# Generated by Django 3.2.13 on 2022-07-11 13:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0004_auto_20220711_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='e2etestactionmodel',
            old_name='e2e_test_id',
            new_name='e2e_test_params',
        ),
        migrations.AlterField(
            model_name='e2etestparamsmodel',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 11, 13, 12, 32, 74642)),
        ),
    ]
