# Generated by Django 3.0 on 2019-12-09 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0009_alertstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertstats',
            name='other_clicks',
            field=models.BigIntegerField(default=0),
        ),
    ]
