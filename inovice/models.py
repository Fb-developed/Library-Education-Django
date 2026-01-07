from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    name = models.CharField(max_length=255)
    invoice_code = models.IntegerField()
    amount_total = models.FloatField()
    maorif_percent = models.FloatField()
    institution_amount = models.FloatField()
    paid_amount = models.FloatField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    loan = models.ForeignKey(
        'book.BookLoan',
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    def __str__(self):
        return f"Invoice #{self.invoice_code} - {self.name}"
