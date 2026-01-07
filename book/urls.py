    # book/urls.py

from django.urls import path
from . import views

app_name = 'book'  # ⬅️ 1. ИН САТРРО ИЛОВА КУНЕД (Барои ислоҳи 'book' is not a namespace)

urlpatterns = [
        path('library/', views.book_list_view, name='book_list'), 
        path('add/', views.add_book_view, name='add_book'),
        
        # ⬅️ 2. ИН САТРРО ИЛОВА КУНЕД (Барои ислоҳи NoReverseMatch 'update_book')
        path('update/<int:pk>/', views.update_book_view, name='update_book'),
    ]