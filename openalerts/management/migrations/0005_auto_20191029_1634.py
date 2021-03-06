# Generated by Django 2.2 on 2019-10-29 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_auto_20191029_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='custom_hostname',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, default='', help_text="Your organization's description (try to keep this under 250 characters)."),
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo_url',
            field=models.URLField(blank=True, default='', help_text="The URL of your news organization's logo (for use on public facing pages)."),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(help_text='The name of your news organization (e.g. The New York Times).', max_length=128),
        ),
        migrations.AlterField(
            model_name='organization',
            name='primary_color',
            field=models.CharField(default='#444444', help_text="Your news organization's primary brand color.", max_length=7),
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.URLField(blank=True, default='', help_text='The full URL of your website (e.g. https://nytimes.com).'),
        ),
    ]
