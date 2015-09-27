# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import chores.models


class Migration(migrations.Migration):

    dependencies = [
        ('chores', '0003_auto_20150927_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chores',
            name='last_completed_by',
            field=models.ForeignKey(related_name='last_completed_by', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chores',
            name='last_completed_date',
            field=models.DateTimeField(default=chores.models.last_year),
        ),
        migrations.AlterField(
            model_name='chores',
            name='primary_assignee',
            field=models.ForeignKey(related_name='primary_assignee', default=2, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='history',
            name='complete_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
