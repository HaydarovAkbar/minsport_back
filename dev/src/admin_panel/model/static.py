from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify

from admin_panel.common import generate_field


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


class StaticPage(models.Model):
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500, null=True)
    slug = models.SlugField(unique=True, max_length=200, null=True)
    content = models.TextField()
    views = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'static_pages'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.url) != self.slug:
                self.slug = generate_unique_slug(StaticPage, self.url)
        else:  # create
            self.slug = generate_unique_slug(StaticPage, self.url)

        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)

        super(StaticPage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
