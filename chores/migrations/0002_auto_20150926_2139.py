# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complete_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ('-complete_date', '-id'),
            },
        ),
        migrations.AddField(
            model_name='chores',
            name='category',
            field=models.ForeignKey(default='', to='chores.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chores',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='chore',
            field=models.ForeignKey(to='chores.Chores'),
        ),
        migrations.AddField(
            model_name='history',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
