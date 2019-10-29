# Generated by Django 2.2 on 2019-10-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_organization_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='logo_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='primary_color',
            field=models.CharField(default='#444444', max_length=7),
        ),
    ]