# Generated by Django 3.2.13 on 2022-07-22 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0014_auto_20220722_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='e2etestresultsmodel',
            old_name='error_detail',
            new_name='failed_details',
        ),
        migrations.AlterField(
            model_name='e2etestparamsmodel',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 7, 22, 12, 28, 6, 232648)),
        ),
    ]
