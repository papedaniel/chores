from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from datetime import datetime
from django.contrib.auth.models import User

class History(models.Model):
    chore = models.ForeignKey('chores.Chores')
    complete_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        ordering = ('-complete_date', '-id')

    def __unicode__(self):
        return '{} {}'.format(self.comment, self.blog)


class Chores(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey('chores.Category')
    primary_assignee = models.ForeignKey(User, null=True, blank=True, related_name='primary_assignee')
    secondary_assignee = models.ForeignKey(User, null=True, blank=True, related_name='secondary_assignee')
    frequency_in_days = models.IntegerField(default=0)
    last_completed_date = models.DateTimeField(default=datetime.now)
    last_completed_by = models.ForeignKey(User, null=True, blank=True, related_name='last_completed_by')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Chores, self).save()

    def __unicode__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('-id', )

    @permalink
    def get_absolute_url(self):
        return 'view_blog_post', None, {'slug': self.slug}


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Category, self).save()

    def __unicode__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('title', )

    @permalink
    def get_absolute_url(self):
        return 'view_category', None, {'slug': self.slug}
