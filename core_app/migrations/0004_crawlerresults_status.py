# Generated by Django 3.2.13 on 2022-06-05 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0003_rename_crawlertask_crawlerresults'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlerresults',
            name='status',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
