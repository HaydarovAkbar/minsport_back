from django.db import models
from sorl.thumbnail import ImageField
# from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.conf import settings

from admin_panel.common import generate_field
from admin_panel.model.territorial import Region, District
from admin_panel.model.ministry import Organization, Staff


class Service(models.Model):
    title = models.CharField(max_length=500, null=True, blank=False)
    icon = models.FileField(upload_to='icon', null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    # content = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'service'
        ordering = ['order', 'created_at']

    def __str__(self):
        return str(self.title)

    def icon_url(self):
        if self.icon:
            return '%s%s' % (settings.HOST, self.icon.url) if self.icon else ""

        return ''

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Service, self).save(*args, **kwargs)


class EmployeeRating(models.Model):
    Admission = 1
    Rank = 2
    Passport = 3

    Perfect = 5
    Good = 4
    Unsatisfactory = 3

    service_choice = (
        (Admission, "Sport ta'lim muassasalarini qabul qilish"),
        (Rank, "Sport unvonlari va sport razryadlarini berish"),
        (Passport, "Sportchi passporti berish"),
    )

    grade_choice = (
        (Perfect, 'Perfect'),
        (Good, 'Good'),
        (Unsatisfactory, 'Unsatisfactory'),
    )

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    employee = models.ForeignKey(Staff, on_delete=models.CASCADE)
    service_type = models.IntegerField(choices=service_choice, default=0)
    grade_type = models.IntegerField(choices=grade_choice, default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'employee_rating'


# from .territorial import Region, District
#
#
# class Participants(models.Model):
#     firstname = models.CharField(max_length=150, blank=True)
#     lastname = models.CharField(max_length=150, blank=True)
#     middlename = models.CharField(max_length=150, blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     place_of_birth = models.CharField(max_length=150, blank=True)
#     position = models.CharField(max_length=150, blank=True)
#     education = models.CharField(max_length=150, blank=True)
#     experience = models.CharField(max_length=150, blank=True)
#     phone = models.CharField(max_length=150, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
#     district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
#     image = models.ImageField(upload_to='participants', null=True, blank=False)
#
#     class Meta:
#         db_table = 'participant'
#
#     def __str__(self):
#         return str(self.firstname)
#
#     @property
#     def image_url(self):
#         # "Returns the image url."
#         if self.image:
#             return '%s%s' % (settings.HOST, self.image.url)
#         return ''
#
#
# class EvolutionCriteria(models.Model):
#     title = models.CharField(max_length=150, blank=True)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.BooleanField(default=False, blank=True)
#     image = models.ImageField(upload_to='evolution_criteria', null=True, blank=False)
#
#     class Meta:
#         db_table = 'evolution_criteria'
#
#     def __str__(self):
#         return str(self.title)
#
#
# class Rating(models.Model):
#     participant = models.ForeignKey(Participants, on_delete=models.CASCADE, null=True, blank=True)
#     evolution_criteria = models.ForeignKey(EvolutionCriteria, on_delete=models.CASCADE, null=True, blank=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#     score = models.IntegerField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'rating'
#
#     def __str__(self):
#         return str(self.score)
