# Generated by Django 3.1 on 2021-05-10 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0004_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(default='theorangeyakco', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='donations.company'),
        ),
    ]