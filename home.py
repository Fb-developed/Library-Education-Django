from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from book.models import Book, BookLoan
from students.models import Student, Institution

@login_required 
def home_view(request):
    user = request.user
    is_admin = user.is_superuser or user.is_staff

    if is_admin:
        books_count = Book.objects.count()
        students_count = Student.objects.count()
        institutions_count = Institution.objects.count()
        loans_count = BookLoan.objects.count()
    elif user.institution:
        books_count = Book.objects.filter(institution=user.institution).count()
        students_count = Student.objects.filter(institution=user.institution).count()
        institutions_count = Institution.objects.filter(pk=user.institution_id).count()
        loans_count = BookLoan.objects.filter(institution=user.institution).count()
    else:
        books_count = 0
        students_count = 0
        institutions_count = 0
        loans_count = 0

    context = {
        'books_count': books_count,
        'students_count': students_count,
        'institutions_count': institutions_count,
        'loans_count': loans_count,
    }
    return render(request, 'dashboard/home.html', context)
