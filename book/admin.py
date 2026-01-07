from django.contrib import admin
from .models import Book, BookLoan, BookPriceFactor


admin.site.register(Book)
admin.site.register(BookLoan)
admin.site.register(BookPriceFactor)