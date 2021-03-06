# Generated by Django 3.0 on 2019-12-03 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0007_auto_20191203_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='content',
            field=models.TextField(db_index=True, help_text='What is the content of the alert? We recommend keeping this under 250 characters.'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='published',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='url',
            field=models.URLField(blank=True, db_index=True, help_text='Where should subscribers go when they click on the alert? (Usually, this is the link to the associated news story on your website.)'),
        ),
    ]
