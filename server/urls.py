from django.contrib import admin
from django.urls import path, include
from home import home_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('autho/',include('accounts.urls')),
    path('',home_view, name="home"),
    path('student/',include('students.urls')),
    path('book/',include('book.urls')),
]
