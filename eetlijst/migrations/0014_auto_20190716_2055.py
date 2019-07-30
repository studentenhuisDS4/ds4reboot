# Generated by Django 2.1.9 on 2019-07-16 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eetlijst', '0013_dinner_cost_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dinner',
            name='eta_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='userdinner',
            name='dinner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eetlijst.Dinner', null=True),
        ),
    ]
