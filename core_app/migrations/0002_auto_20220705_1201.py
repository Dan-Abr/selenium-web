# Generated by Django 3.2.13 on 2022-07-05 12:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='e2etestresultsmodel',
            name='e2e_test_params',
        ),
        migrations.AlterField(
            model_name='e2etestparamsmodel',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 5, 12, 1, 4, 286832)),
        ),
    ]