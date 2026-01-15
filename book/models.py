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
    price_from = models.FloatField(blank=True, null=True, verbose_name="Нарх аз")
    price_to = models.FloatField(blank=True, null=True, verbose_name="Нарх то")
    year_from = models.IntegerField(blank=True, null=True, verbose_name="Соли нашр аз")
    year_to = models.IntegerField(blank=True, null=True, verbose_name="Соли нашр то")
    description = models.TextField(blank=True, null=True, verbose_name="Шарҳу эзоҳ")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Фоизнокии иҷораи китоб"
        verbose_name_plural = "Фоизнокии иҷораи китоб"
        ordering = ['-factor', 'label']

    def __str__(self):
        return f"{self.label} ({self.percent_value:.2f}%)"
    
    @property
    def percent_value(self):
        """Returns normalized percent value regardless of stored format."""
        return self.factor * 100 if self.factor <= 1 else self.factor

    @classmethod
    def lookup_percent(cls, book_price, book_year):
        """Find the best matching percent for provided price/year."""
        factors = cls.objects.all()
        if not factors.exists():
            return 0

        price_candidates = factors.filter(
            models.Q(price_from__isnull=True) | models.Q(price_from__lte=book_price),
            models.Q(price_to__isnull=True) | models.Q(price_to__gte=book_price),
        )
        if not price_candidates.exists():
            price_candidates = factors

        def year_distance(factor):
            start = factor.year_from
            end = factor.year_to
            if start is None and end is None:
                return float('inf')
            if start is None:
                return 0 if book_year <= end else book_year - end
            if end is None:
                return 0 if book_year >= start else start - book_year
            if start <= book_year <= end:
                return 0
            if book_year < start:
                return start - book_year
            return book_year - end

        def year_span(factor):
            if factor.year_from is None or factor.year_to is None:
                return float('inf')
            return factor.year_to - factor.year_from

        best_factor = sorted(
            price_candidates,
            key=lambda factor: (year_distance(factor), year_span(factor), -factor.percent_value),
        )[0]
        return best_factor.percent_value
