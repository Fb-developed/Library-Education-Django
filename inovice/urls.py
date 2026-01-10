from django.urls import path
from . import views

urlpatterns = [
    path('bookpayments/', views.payments_list_view, name='payments_list'),
]
