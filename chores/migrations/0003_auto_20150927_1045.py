# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chores', '0002_auto_20150926_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chores',
            name='user',
        ),
        migrations.AddField(
            model_name='chores',
            name='frequency_in_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chores',
            name='last_completed_by',
            field=models.ForeignKey(related_name='last_completed_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='chores',
            name='last_completed_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='chores',
            name='primary_assignee',
            field=models.ForeignKey(related_name='primary_assignee', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='chores',
            name='secondary_assignee',
            field=models.ForeignKey(related_name='secondary_assignee', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
