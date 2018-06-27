# Generated by Django 2.0.6 on 2018-06-26 15:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180626_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 6, 26, 15, 16, 57, 742355, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]