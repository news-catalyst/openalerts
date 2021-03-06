# Generated by Django 3.0 on 2019-12-03 17:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_webpushsubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailsubscription',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webpushsubscription',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
