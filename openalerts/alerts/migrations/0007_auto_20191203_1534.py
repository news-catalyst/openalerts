# Generated by Django 3.0 on 2019-12-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0006_auto_20191113_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='human_readable_identifier',
            field=models.TextField(blank=True, default='', help_text="On Twitter, for example, this is the account's @username."),
        ),
        migrations.AlterField(
            model_name='source',
            name='identifier',
            field=models.TextField(blank=True, null=True),
        ),
    ]
