# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_housemate_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='housemate',
            name='boetes',
            field=models.IntegerField(default=0),
        ),
    ]
