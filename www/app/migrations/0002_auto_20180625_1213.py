# Generated by Django 2.0.6 on 2018-06-25 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapitem',
            name='adress',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapitem',
            name='object',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
