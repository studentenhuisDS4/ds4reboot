# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 12:25
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eetlijst', '0004_auto_20160311_0152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datelist',
            old_name='list_open',
            new_name='open',
        ),
        migrations.RenameField(
            model_name='userlist',
            old_name='list_timestamp',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='userlist',
            old_name='list_user',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='datelist',
            name='list_cost',
        ),
        migrations.RemoveField(
            model_name='datelist',
            name='list_date',
        ),
        migrations.AddField(
            model_name='datelist',
            name='close_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='datelist',
            name='cook',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='datelist',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='datelist',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 3, 11, 12, 25, 44, 334458, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datelist',
            name='signup_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userlist',
            name='list_count',
            field=models.IntegerField(default=0),
        ),
    ]