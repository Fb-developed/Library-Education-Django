from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from book.models import Book, BookLoan, BookPriceFactor
from inovice.models import Invoice
from .models import Institution, Region, Student


class LoanInvoiceTests(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Регион")
        self.institution = Institution.objects.create(
            name="Муассиса 1",
            address="Суроға",
            phone="123",
            year=2020,
            status=True,
            type="Макт",
            region=self.region,
            institution_percent=3,
        )
        self.user = get_user_model().objects.create_user(
            username="user1",
            email="user1@example.com",
            password="pass1234",
            institution=self.institution,
        )
        self.student = Student.objects.create(
            fullname="Хонанда 1",
            class_number=5,
            class_latter="А",
            institution=self.institution,
        )
        self.book = Book.objects.create(
            name="Китоб 1",
            price=100,
            class_number=5,
            year=2020,
            quantity_total=1,
            quantity_available=1,
            institution=self.institution,
        )
        BookPriceFactor.objects.create(
            label="2020",
            factor=2,
            year_from=2019,
            year_to=2021,
            price_from=0,
            price_to=200,
        )

    def test_give_book_creates_invoice(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('give_book_to_student', args=[self.student.id]),
            data={'book_id': self.book.id, 'year_of_use': '2024'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookLoan.objects.count(), 1)
        self.assertEqual(Invoice.objects.count(), 1)

        invoice = Invoice.objects.first()
        self.assertAlmostEqual(invoice.amount_total, 5)
        self.assertAlmostEqual(invoice.maorif_percent, 2)
        self.assertAlmostEqual(invoice.institution_amount, 3)
        self.assertEqual(invoice.paid_amount, 0)


class DashboardCountsTests(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Регион")
        self.institution = Institution.objects.create(
            name="Муассиса 2",
            address="Суроға",
            phone="456",
            year=2021,
            status=True,
            type="Макт",
            region=self.region,
        )
        self.user = get_user_model().objects.create_user(
            username="user2",
            email="user2@example.com",
            password="pass1234",
            institution=self.institution,
        )
        self.student = Student.objects.create(
            fullname="Хонанда 2",
            class_number=6,
            class_latter="Б",
            institution=self.institution,
        )
        self.book = Book.objects.create(
            name="Китоб 2",
            price=120,
            class_number=6,
            year=2021,
            quantity_total=2,
            quantity_available=2,
            institution=self.institution,
        )
        BookLoan.objects.create(
            student=self.student,
            book=self.book,
            institution=self.institution,
            loan_date=timezone.now(),
            return_date=timezone.now() + timedelta(days=365),
            class_number=self.student.class_number,
            year=self.book.year,
            year_of_use=timezone.now().year,
            calculated_price=10,
        )

    def test_dashboard_counts_for_institution(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))

        self.assertEqual(response.context['books_count'], 1)
        self.assertEqual(response.context['students_count'], 1)
        self.assertEqual(response.context['institutions_count'], 1)
        self.assertEqual(response.context['loans_count'], 1)
