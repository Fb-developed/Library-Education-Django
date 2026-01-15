from django.db import models
from django.utils import timezone


class Region(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField()
    institution_percent = models.FloatField(default=0, verbose_name="Фоизи муассиса")
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    region = models.ForeignKey(
        'Region',
        on_delete=models.CASCADE,
        related_name='institutions'
    )

    def __str__(self):
        return self.name

    @property
    def region_name(self):
        return self.region.name if self.region else ""


class Student(models.Model):
    fullname = models.CharField(max_length=255)
    class_number = models.IntegerField()
    class_latter = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)

    institution = models.ForeignKey(
        'Institution',
        on_delete=models.CASCADE,
        related_name='students'
    )

    def __str__(self):
        return self.fullname

    @property
    def institution_name(self):
        return self.institution.name if self.institution else ""
