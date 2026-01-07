from django.urls import path
from . import views # Ин кор мекунад

urlpatterns = [
    path('muasisaho/',views.muasisaho_list_view, name='muasisaho_list'),
    path('khonandagon/', views.khonandagon_list_view, name='khonandagon_list'),
    path('khonandagon/add/', views.add_khonanda_view, name='add_khonanda'), 
    path('khonandagon/edit/<int:pk>/', views.student_edit_view, name='student_edit'), # ИСТИФОДАИ views.
    path('khonandagon/give-book/<int:pk>/', views.give_book_to_student_view, name='give_book_to_student'),
]