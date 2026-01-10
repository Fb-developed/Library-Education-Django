from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    name = models.CharField(max_length=255)
    invoice_code = models.BigIntegerField()  # Changed to BigInteger for larger numbers
    amount_total = models.FloatField()
    maorif_percent = models.FloatField()  # 2% of education department
    institution_amount = models.FloatField()
    paid_amount = models.FloatField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    payment_date = models.DateTimeField(null=True, blank=True)  # Last payment date

    loan = models.ForeignKey(
        'book.BookLoan',
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Пардохт"
        verbose_name_plural = "Пардохтҳо"

    def __str__(self):
        return f"Invoice #{self.invoice_code} - {self.name}"
    
    @property
    def is_paid(self):
        """Check if invoice is fully paid"""
        return self.status and self.paid_amount >= self.amount_total