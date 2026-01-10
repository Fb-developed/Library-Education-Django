from django.contrib import admin
from django.urls import path, include
from home import home_view
from book import views as book_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('autho/',include('accounts.urls')),
    path('',home_view, name="home"),
    path('student/',include('students.urls')),
    path('book/',include('book.urls')),
    path('categories/', book_views.book_price_factor_list_view, name='categories'),  # Alias for book price factors
    path('', include('inovice.urls')),  # Payments URLs
]
