    # book/urls.py

from django.urls import path
from . import views

app_name = 'book'  # ⬅️ 1. ИН САТРРО ИЛОВА КУНЕД (Барои ислоҳи 'book' is not a namespace)

urlpatterns = [
        path('library/', views.book_list_view, name='book_list'), 
        path('add/', views.add_book_view, name='add_book'),
        path('update/<int:pk>/', views.update_book_view, name='update_book'),
        path('price-factors/', views.book_price_factor_list_view, name='price_factors'),
        path('price-factors/add/', views.book_price_factor_create_view, name='price_factors_add'),
        path('price-factors/<int:pk>/edit/', views.book_price_factor_update_view, name='price_factors_edit'),
    ]
