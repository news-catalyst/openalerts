# Generated by Django 2.2 on 2019-10-28 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20191023_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
