# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_operations', '0002_auto_20170805_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='type_0',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_operations.Types', verbose_name='Type_id'),
        ),
    ]
