# Generated by Django 2.1.9 on 2019-07-25 09:12

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eetlijst', '0015_auto_20190725_1032'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='holog',
            new_name='splittransfer'
        ),
        migrations.AddField(
            model_name='splittransfer',
            name='affected_users',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
        migrations.AddField(
            model_name='splittransfer',
            name='delta_remainder',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.RenameField(
            model_name='splittransfer',
            old_name='total_balance',
            new_name='total_balance_after', ),
        migrations.AddField(
            model_name='splittransfer',
            name='total_balance_before',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, null=True)
        ),

    ]