# Generated by Django 3.1 on 2021-05-14 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0006_auto_20210510_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='domains',
        ),
        migrations.AddField(
            model_name='company',
            name='rzp_identifier_key',
            field=models.CharField(default='Organisation', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='rzp_identifier_value',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
