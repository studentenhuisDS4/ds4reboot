# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-13 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20160828_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='housemate',
            name='activate_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='housemate',
            name='inactivate_date',
            field=models.DateField(null=True),
        ),
    ]
