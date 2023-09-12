from django.conf import settings
from django.db import models
from django.utils import timezone
from sorl.thumbnail import ImageField
# from django.utils.translation import ugettext_lazy as _

from admin_panel.common import generate_field
from admin_panel.model.territorial import Region


class Type(models.Model):
    title = models.CharField(max_length=600)
    primary = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tender_type'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Type, self).save(*args, **kwargs)


class Tender(models.Model):
    title = models.CharField(max_length=500)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    number = models.IntegerField(default=0, blank=True)
    organizer = models.CharField(max_length=500)
    file = models.FileField(upload_to='tender')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    is_published = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tender'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    @property
    def file_url(self):
        if self.file:
            # Return file url
            return '%s%s' % (settings.HOST, self.file.url)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.organizer_uz:
            self.organizer_sr = generate_field(self.organizer_uz)

        super(Tender, self).save(*args, **kwargs)
