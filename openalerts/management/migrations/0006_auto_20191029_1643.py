# Generated by Django 2.2 on 2019-10-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_auto_20191029_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='custom_hostname',
            field=models.TextField(blank=True, help_text="Your organization's custom hostname (domain) for OpenAlerts. If you don't know what this means, just ignore it.", null=True, unique=True),
        ),
    ]
