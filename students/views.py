# home/views.py (ё views.py-и барномаи дахлдор)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Institution, Student, Region # Фарз мекунем, ки моделҳо дар ин ҷо ҳастанд, агар не, онро дуруст import кунед!
from book.models import Book, BookLoan


# --- [НАВСОЗӢ] View барои Муассисаҳо ---
@login_required
def muasisaho_list_view(request):
    # Гирифтани ҳамаи муассисаҳо. select_related('region') барои оптимизатсияи query.
    all_institutions = Institution.objects.select_related('region').all()
    
    context = {
        # Барои истифода дар шаблони HTML:
        'muasisaho': all_institutions,
        'total_count': all_institutions.count(),
    } 
    return render(request, 'dashboard/muasisaho_list.html', context)
    
    
# --- [НАВСОЗӢ] View барои Хонандагон ---
@login_required
def khonandagon_list_view(request):
    # 1. МУАССИСАИ КОРБАРИ ҶОРӢ:
    # Фарз мекунем, ки корбар (request.user) ба муассисаи мушаххас пайваст аст.
    # Масалан, тавассути хосияти 'institution' дар модели User ё Profile.
    
    # !!! ДИҚҚАТ: Ин сатрҳоро мувофиқи тарҳи воқеии корбари худ тағйир диҳед!
    # Намунаи 1: Агар Institution FK бевосита дар User бошад:
    user_institution = request.user.institution
    # Намунаи 2: Агар тавассути Profile бошад:
    # user_institution = request.user.profile.institution
    
    if not user_institution:
        # Агар корбар ба ҳеҷ муассиса пайваст набошад, рӯйхати холӣ баргардонед.
        return render(request, 'dashboard/khonandagon_list.html', {'khonandagon': [], 'total_count': 0})

    # Филтри асосӣ: Танҳо хонандагони муассисаи корбар
    students_queryset = Student.objects.filter(
        institution=user_institution
    ).select_related('institution', 'institution__region') # Оптимизатсия

    # 2. ФИЛТРАТСИЯИ ҶУСТУҶӮ (Search/Filtering):
    
    # Филтри Синф (class_number: 1 то 11)
    sinf = request.GET.get('sinf')
    if sinf and sinf.isdigit():
        students_queryset = students_queryset.filter(class_number=int(sinf))

    # Филтри Ному насаб (fullname) - ҷустуҷӯи нопурра (icontains)
    fullname = request.GET.get('fullname')
    if fullname:
        students_queryset = students_queryset.filter(
            Q(fullname__icontains=fullname)
        )
        
    # Филтри Гурӯҳ (class_latter) - ҷустуҷӯи нопурра (icontains)
    guruh = request.GET.get('guruh')
    if guruh:
        # Агар шумо SELECT-ро истифода баред, одатан ҷустуҷӯи дақиқтар лозим аст (exact match)
        students_queryset = students_queryset.filter(class_latter__iexact=guruh)
    
    # Натиҷаҳои ниҳоӣ
    all_students = students_queryset.order_by('class_number', 'class_latter', 'fullname')
    
    context = {
        'khonandagon': all_students,
        'total_count': all_students.count(),
        # Барои нигоҳ доштани арзишҳои форма ҳангоми бозгашт
        'sinf_value': sinf,
        'fullname_value': fullname,
        'guruh_value': guruh,
    } 
    return render(request, 'dashboard/khonandagon_list.html', context)



@login_required
def add_khonanda_view(request):
    # !!! ДИҚҚАТ: Муассисаи корбари ҷориро гиред (ҳамчун қадами қаблӣ)
    user_institution = request.user.institution # Фарз мекунем, ки пайваст аст

    # Тафтиш кардан, ки корбар ба муассиса пайваст аст ё не
    if not user_institution:
        error_message = "Шумо ба муассиса пайваст нашудаед. Лутфан бо мудир тамос гиред."
        sinfho = range(1, 12)
        guruhho = ['А', 'Б', 'В', 'Г', 'Д']
        context = {
            'error': error_message,
            'sinfho': sinfho,
            'guruhho': guruhho,
        }
        return render(request, 'dashboard/add_khonanda.html', context)

    if request.method == 'POST':
        # Гирифтани маълумот аз форма
        fullname = request.POST.get('fullname')
        sinf = request.POST.get('sinf')
        guruh = request.POST.get('guruh')
        suroga = request.POST.get('suroga')

        try:
            # Тафтиши арзишҳои асосӣ
            if not all([fullname, sinf, guruh]):
                raise ValueError("Лутфан ҳамаи майдонҳои заруриро пур кунед.")
            
            # Тафтиш кардан, ки муассиса мавҷуд аст
            if not user_institution:
                raise ValueError("Шумо ба муассиса пайваст нашудаед. Лутфан бо мудир тамос гиред.")
            
            # Эҷоди объекти нав
            Student.objects.create(
                fullname=fullname,
                class_number=int(sinf),
                class_latter=guruh,
                institution=user_institution, # Пайваст кардан ба муассисаи корбар
                # Агар дар модели Student майдони suroga вуҷуд дошта бошад, онро илова кунед
                # address=suroga, 
            )
            
            # Пас аз сабти муваффақ, ба рӯйхати хонандагон равона кунед
            return redirect('khonandagon_list') 

        except ValueError as e:
            # Дар сурати хатогӣ, формаро бо хабар боз нишон диҳед
            sinfho = range(1, 12)
            guruhho = ['А', 'Б', 'В', 'Г', 'Д']
            context = {
                'error': str(e),
                # Барои нигоҳ доштани маълумоти воридшуда
                'fullname_value': fullname, 
                'sinf_value': sinf,
                'guruh_value': guruh,
                'suroga_value': suroga,
                'sinfho': sinfho,
                'guruhho': guruhho,
            }
            return render(request, 'dashboard/add_khonanda.html', context)
        except Exception as e:
            # Барои дигар хатогиҳо
            sinfho = range(1, 12)
            guruhho = ['А', 'Б', 'В', 'Г', 'Д']
            context = {
                'error': f"Хатогӣ: {str(e)}",
                'fullname_value': fullname, 
                'sinf_value': sinf,
                'guruh_value': guruh,
                'suroga_value': suroga,
                'sinfho': sinfho,
                'guruhho': guruhho,
            }
            return render(request, 'dashboard/add_khonanda.html', context)

    # Агар request GET бошад, формаи холиро нишон диҳед
    # Маълумот барои интихобкунандаи Синф
    sinfho = range(1, 12)
    guruhho = ['А', 'Б', 'В', 'Г', 'Д']
    
    context = {
        'sinfho': sinfho,
        'guruhho': guruhho,
    }
    return render(request, 'dashboard/add_khonanda.html', context)




@login_required
def student_edit_view(request, pk):
    user_institution = request.user.institution
    
    if not user_institution:
        return redirect('khonandagon_list')
    
    # Гирифтани хонанда ва тафтиш кардан, ки ба муассисаи корбар тааллуқ дорад
    student = get_object_or_404(Student, pk=pk, institution=user_institution)
    
    if request.method == 'POST':
        # Гирифтани маълумот аз форма
        fullname = request.POST.get('fullname')
        sinf = request.POST.get('sinf')
        guruh = request.POST.get('guruh')
        suroga = request.POST.get('suroga', '')
        
        try:
            # Тафтиши арзишҳои асосӣ
            if not all([fullname, sinf, guruh]):
                raise ValueError("Лутфан ҳамаи майдонҳои заруриро пур кунед.")
            
            # Навсозии маълумот
            student.fullname = fullname
            student.class_number = int(sinf)
            student.class_latter = guruh
            student.save()
            
            # Пас аз навсозии муваффақ, ба рӯйхати хонандагон равона кунед
            return redirect('khonandagon_list')
            
        except ValueError as e:
            # Дар сурати хатогӣ, формаро бо хабар боз нишон диҳед
            sinfho = range(1, 12)
            guruhho = ['А', 'Б', 'В', 'Г', 'Д']
            context = {
                'error': str(e),
                'student': student,
                'fullname_value': fullname,
                'sinf_value': sinf,
                'guruh_value': guruh,
                'suroga_value': suroga,
                'sinfho': sinfho,
                'guruhho': guruhho,
            }
            return render(request, 'dashboard/edit_khonanda.html', context)
        except Exception as e:
            sinfho = range(1, 12)
            guruhho = ['А', 'Б', 'В', 'Г', 'Д']
            context = {
                'error': f"Хатогӣ: {str(e)}",
                'student': student,
                'fullname_value': request.POST.get('fullname', ''),
                'sinf_value': request.POST.get('sinf', ''),
                'guruh_value': request.POST.get('guruh', ''),
                'suroga_value': request.POST.get('suroga', ''),
                'sinfho': sinfho,
                'guruhho': guruhho,
            }
            return render(request, 'dashboard/edit_khonanda.html', context)
    
    # Агар request GET бошад, формаро бо маълумоти мавҷуда пур кунед
    sinfho = range(1, 12)
    guruhho = ['А', 'Б', 'В', 'Г', 'Д']
    
    context = {
        'student': student,
        'fullname_value': student.fullname,
        'sinf_value': student.class_number,
        'guruh_value': student.class_latter,
        'suroga_value': '',
        'sinfho': sinfho,
        'guruhho': guruhho,
    }
    return render(request, 'dashboard/edit_khonanda.html', context)


@login_required
def give_book_to_student_view(request, pk):
    user_institution = request.user.institution
    
    if not user_institution:
        return redirect('khonandagon_list')
    
    # Гирифтани хонанда ва тафтиш кардан, ки ба муассисаи корбар тааллуқ дорад
    student = get_object_or_404(Student, pk=pk, institution=user_institution)
    
    # Гирифтани китобҳои дастраси муассиса
    available_books = Book.objects.filter(
        institution=user_institution,
        quantity_available__gt=0
    ).order_by('name', 'class_number')
    
    # Гирифтани китобҳои иҷорадодашудаи ин хонанда
    student_loans = BookLoan.objects.filter(
        student=student,
        institution=user_institution
    ).select_related('book').order_by('-loan_date')
    
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        year_of_use = request.POST.get('year_of_use')
        
        try:
            if not book_id:
                raise ValueError("Лутфан китобро интихоб кунед.")
            
            book = get_object_or_404(Book, pk=book_id, institution=user_institution)
            
            # Тафтиш кардан, ки китоб дастрас аст
            if book.quantity_available <= 0:
                raise ValueError("Ин китоб дастрас нест.")
            
            # Ҳисоб кардани маблағи иҷора
            # Фарз мекунем, ки маблағи иҷора = нархи китоб * фактори иҷора
            # Барои соддатарин, маблағи иҷораро ба нархи китоб баробар мегирем
            calculated_price = book.price
            
            # Ҳисоб кардани санаҳо
            loan_date = timezone.now()
            # Фарз мекунем, ки мӯҳлати иҷора 1 сол аст
            return_date = loan_date + timedelta(days=365)
            
            # Эҷоди BookLoan
            loan = BookLoan.objects.create(
                student=student,
                book=book,
                institution=user_institution,
                loan_date=loan_date,
                return_date=return_date,
                class_number=student.class_number,
                year=book.year,
                year_of_use=int(year_of_use) if year_of_use else datetime.now().year,
                calculated_price=calculated_price,
            )
            
            # Кам кардани миқдори боқимондаи китоб
            book.quantity_available -= 1
            book.save()
            
            # Пас аз сабти муваффақ, ба рӯйхати хонандагон равона кунед
            return redirect('khonandagon_list')
            
        except ValueError as e:
            context = {
                'error': str(e),
                'student': student,
                'available_books': available_books,
                'student_loans': student_loans,
                'year_of_use': year_of_use if 'year_of_use' in locals() else datetime.now().year,
            }
            return render(request, 'dashboard/give_book_to_student.html', context)
        except Exception as e:
            context = {
                'error': f"Хатогӣ: {str(e)}",
                'student': student,
                'available_books': available_books,
                'student_loans': student_loans,
                'year_of_use': datetime.now().year,
            }
            return render(request, 'dashboard/give_book_to_student.html', context)
    
    # Агар request GET бошад
    context = {
        'student': student,
        'available_books': available_books,
        'student_loans': student_loans,
        'year_of_use': datetime.now().year,
    }
    return render(request, 'dashboard/give_book_to_student.html', context)


@login_required
def regions_list_view(request):
    """View барои нишон додани рӯйхати ноҳияҳо"""
    all_regions = Region.objects.all().order_by('name')
    
    context = {
        'regions': all_regions,
        'total_count': all_regions.count(),
    }
    return render(request, 'dashboard/regions_list.html', context)


@login_required
def education_departments_list_view(request):
    """View барои нишон додани рӯйхати шуъбаҳои маориф"""
    # Барои ҳозир, рӯйхати холӣ бармегардонем
    # Агар модел мавҷуд бошад, онро истифода баред
    context = {
        'departments': [],
        'total_count': 0,
    }
    return render(request, 'dashboard/education_departments_list.html', context)