# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-25 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0002_provider_user_details_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='services_offered',
        ),
        migrations.AlterField(
            model_name='provider',
            name='healthier_id',
            field=models.CharField(default='provider_r8tjpgwuyrx6l72i5wk0', max_length=30),
        ),
    ]