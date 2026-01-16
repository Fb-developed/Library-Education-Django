from django.urls import path
from . import views

urlpatterns = [
    path('bookpayments/', views.payments_list_view, name='payments_list'),
    path('bookpayments/<int:pk>/paid/', views.mark_payment_paid_view, name='payments_mark_paid'),
]
