from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from datetime import datetime
from django.contrib.auth.models import User

class Comment(models.Model):
    comment = models.TextField()
    publishDate = models.DateTimeField(default=datetime.now)
    blog = models.ForeignKey('blog.Blog')
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        ordering = ('-publishDate', '-id')

    def __unicode__(self):
        return '{} {}'.format(self.comment, self.blog)

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(default=datetime.now)
    edited = models.DateTimeField(default=datetime.now)
    published = models.BooleanField(default=False, null=False)
    category = models.ForeignKey('blog.Category')
    user = models.ForeignKey(User, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Blog, self).save()

    def __unicode__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ('-published', '-posted', '-id')

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
        return 'view_blog_category', None, {'slug': self.slug}
