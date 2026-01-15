from django.test import TestCase

from .models import BookPriceFactor


class BookPriceFactorLookupTests(TestCase):
    def test_lookup_percent_nearest_year(self):
        BookPriceFactor.objects.create(
            label="2010-2015",
            factor=2,
            year_from=2010,
            year_to=2015,
            price_from=0,
            price_to=100,
        )
        BookPriceFactor.objects.create(
            label="2016-2018",
            factor=3,
            year_from=2016,
            year_to=2018,
            price_from=0,
            price_to=100,
        )

        exact_match = BookPriceFactor.lookup_percent(50, 2017)
        nearest_match = BookPriceFactor.lookup_percent(50, 2021)

        self.assertEqual(exact_match, 3)
        self.assertEqual(nearest_match, 3)
