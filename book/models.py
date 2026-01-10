from django.db import models
from django.utils import timezone


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    class_number = models.IntegerField()
    year = models.IntegerField()
    quantity_total = models.IntegerField()
    quantity_available = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    institution = models.ForeignKey(
        'students.Institution',
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.name

    @property
    def institution_name(self):
        return self.institution.name if self.institution else ""


class BookLoan(models.Model):
    loan_date = models.DateTimeField()
    class_number = models.IntegerField()
    year = models.IntegerField()
    year_of_use = models.IntegerField()
    return_date = models.DateTimeField()
    calculated_price = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    institution = models.ForeignKey(
        'students.Institution',
        on_delete=models.CASCADE,
        related_name='book_loans'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='book_loans'
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='loans'
    )

    def __str__(self):
        return f"{self.book.name} → {self.student.fullname}"


class BookPriceFactor(models.Model):
    label = models.CharField(max_length=255, verbose_name="Номгу")
    factor = models.FloatField(verbose_name="Фоиз аз нархи китоб")
    description = models.TextField(blank=True, null=True, verbose_name="Шарҳу эзоҳ")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Фоизнокии иҷораи китоб"
        verbose_name_plural = "Фоизнокии иҷораи китоб"
        ordering = ['-factor', 'label']

    def __str__(self):
        return f"{self.label} ({self.factor * 100:.2f}%)"
    
    @property
    def percentage(self):
        """Returns factor as percentage"""
        return self.factor * 100
