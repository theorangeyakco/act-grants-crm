# Generated by Django 3.1 on 2021-04-30 07:27

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('domestic', models.BooleanField()),
                ('international', models.BooleanField()),
                ('donor_name', models.CharField(max_length=256)),
                ('donor_email', models.EmailField(max_length=254)),
                ('donor_phone', models.CharField(max_length=16)),
                ('donor_pan', models.CharField(blank=True, max_length=16, null=True)),
                ('donor_address', models.CharField(max_length=2048)),
                ('donor_country', models.CharField(max_length=32)),
                ('donor_zipcode', models.CharField(max_length=16)),
                ('payment_time', models.DateTimeField()),
                ('rzp_response', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
