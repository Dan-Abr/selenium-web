# Generated by Django 3.2.13 on 2022-06-13 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0008_auto_20220611_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='e2etestparams',
            name='enabled',
            field=models.BooleanField(default='True'),
            preserve_default=False,
        ),
    ]