# Generated by Django 2.1.11 on 2019-09-01 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0004_auto_20190902_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='accepted_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_user', to=settings.AUTH_USER_MODEL),
        ),
    ]