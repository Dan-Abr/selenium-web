# Generated by Django 3.2.13 on 2022-08-15 12:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0017_auto_20220812_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='e2etestresultsmodel',
            name='e2e_test_params_pk',
            field=models.IntegerField(default=0, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='e2etestparamsmodel',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 15, 12, 20, 39, 837818)),
        ),
    ]