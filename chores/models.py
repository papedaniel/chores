from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from datetime import datetime
from django.contrib.auth.models import User

class Chores(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

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
