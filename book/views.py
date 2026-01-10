# book/views.py

from django.shortcuts import render, redirect, get_object_or_404 # ⬅️ get_object_or_404-ро ИЛОВА КУНЕД
from django.contrib.auth.decorators import login_required
from .models import Book, BookPriceFactor 
from .forms import BookForm  # ⬅️ ❗️ ИН САТРРО ИЛОВА КУНЕД ❗️
from django.http import HttpResponse # ⬅️ ❗️ ИН САТРРО ИЛОВА КУНЕД ❗️






@login_required
def book_list_view(request):
    user_institution = request.user.institution
    
    if not user_institution:
        # Агар корбар муассиса надошта бошад
        context = {
            'books': [],
            'all_sinfs': [],
            'all_years': [],
            'selected_sinf': None,
            'selected_year': None,
            'total_books_count': 0,
            'total_available': 0,
            'total_deleted': 0,
            'user_institution_name': "Номаълум",
        }
        return render(request, 'dashboard/book_list.html', context)
    
    # Филтри асосӣ ва фармоиш: Истифодаи class_number ба ҷои sinf
    books = Book.objects.filter(institution=user_institution).order_by('class_number', 'name')
    
    # 2. Филтрҳо аз рӯи GET-параметрҳо
    # ❗️ Ислоҳ: sinf_filter -> class_number_filter ❗️
    class_number_filter = request.GET.get('sinf') # Мо дар URL 'sinf'-ро истифода мебарем, аммо дар Query 'class_number'-ро
    year_filter = request.GET.get('year') 
    
    # ❗️ Ислоҳ: Филтрро аз рӯи class_number иҷро кунед ❗️
    if class_number_filter and class_number_filter != '':
        books = books.filter(class_number=class_number_filter)
        
    if year_filter and year_filter != '':
        # Фарз мекунем, ки майдони соли воридшавӣ 'year' аст
        books = books.filter(year=year_filter)

    # 3. Барои имконоти филтр, рӯйхати нотакрори синфҳо ва солҳоро гиред:
    # ❗️ Ислоҳ: Истифодаи class_number ба ҷои sinf ❗️
    all_sinfs = Book.objects.filter(institution=user_institution).values_list('class_number', flat=True).distinct()
    
    # Фарз мекунем, ки майдони соли воридшавӣ 'year' аст
    all_years = Book.objects.filter(institution=user_institution).values_list('year', flat=True).distinct().order_by('-year')

    # Calculate total books count
    total_books_count = books.count()
    
    # Calculate statistics
    total_available = sum(book.quantity_available for book in books)
    total_deleted = sum(getattr(book, 'deleted_count', 0) or 0 for book in books)
    
    # Get institution name
    user_institution_name = user_institution.name if user_institution else "Номаълум"
    
    context = {
        'books': books,
        'all_sinfs': sorted(all_sinfs), 
        'all_years': all_years,
        # ❗️ Ислоҳ: selected_sinf-ро аз class_number_filter гиред ❗️
        'selected_sinf': class_number_filter, 
        'selected_year': year_filter,
        'total_books_count': total_books_count,
        'total_available': total_available,
        'total_deleted': total_deleted,
        'user_institution_name': user_institution_name,
    }
    return render(request, 'dashboard/book_list.html', context)



@login_required
def add_book_view(request):
    if not request.user.institution:
        # Агар корбар муассиса надошта бошад, иҷозат надиҳед
        return redirect('book:book_list') 

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            
            # 1. Муассисаро илова кунед
            book.institution = request.user.institution
            
            # 2. Барои илова, ҳамеша боқимонда ба шумораи умумӣ баробар аст
            # quantity_available-ро аз форма гирифтан лозим нест, зеро он хориҷ карда шудааст
            book.quantity_available = book.quantity_total
            
            try:
                book.save()
                return redirect('book:book_list')
            except Exception as e:
                # Агар хатогӣ рух диҳад, формаро бо хабар боз нишон диҳед
                context = {
                    'form': form,
                    'page_title': 'Иловаи китоби нав',
                    'update': False,
                    'error': f"Хатогӣ: {str(e)}"
                }
                return render(request, 'dashboard/add_book_form.html', context)
        else:
            # Форма нодуруст аст, бо хатогиҳо боз нишон диҳед
            context = {
                'form': form,
                'page_title': 'Иловаи китоби нав',
                'update': False
            }
            return render(request, 'dashboard/add_book_form.html', context)

    else:
        form = BookForm()

    context = {
        'form': form,
        'page_title': 'Иловаи китоби нав',
        'update': False
    }
    return render(request, 'dashboard/add_book_form.html', context)



@login_required
def update_book_view(request, pk):
    # 1. Китобро пайдо кунед ё 404-ро баланд кунед.
    # Боварӣ ҳосил кунед, ки китоб ба муассисаи корбар тааллуқ дорад (барои амният).
    book_instance = get_object_or_404(Book, pk=pk, institution=request.user.institution)
    
    # 2. Логикаи POST (Вақте ки форма фиристода мешавад)
    if request.method == 'POST':
        # Формаро бо маълумоти POST ва instance-и китоб пур кунед
        form = BookForm(request.POST, instance=book_instance)
        
        if form.is_valid():
            # Пеш аз сабт кардани тағйирот, миқдори кӯҳнаро захира кунед
            old_total = book_instance.quantity_total
            
            book = form.save(commit=False)
            new_total = book.quantity_total
            
            # Агар миқдори умумӣ тағйир ёбад, миқдори боқимондаро ҳисоб кунед
            if old_total != new_total:
                # Фарқиятро ҳисоб кунед (афзоиш ё камшавӣ)
                difference = new_total - old_total
                
                # Миқдори боқимондаро бо фарқияти навсозӣ кунед
                book.quantity_available += difference 
            
            book.save()
            return redirect('book:book_list')
        
    # 3. Логикаи GET (Вақте ки саҳифа бори аввал кушода мешавад)
    else:
        # Формаро бо маълумоти мавҷудаи китоб пур кунед
        form = BookForm(instance=book_instance)

    context = {
        'form': form,
        'page_title': f"Тағйир додани китоб: {book_instance.name}",
        'update': True, # Барои истифода дар шаблони HTML (Барои фарқ кардани Add ва Update)
        'book_instance': book_instance, # Барои истифода дар action URL дар HTML
    }
    # Мо ҳамон шаблони add_book_form.html-ро истифода мебарем
    return render(request, 'dashboard/add_book_form.html', context)


@login_required
def book_price_factor_list_view(request):
    """View барои нишон додани рӯйхати фоизнокии иҷораи китоб"""
    # Гирифтани ҳамаи фоизнокиҳо бо фармоиши мувофиқ
    # Аввал бо фоиз нисбӣ (factor) фармоиш медиҳем, сипас бо ном
    price_factors = BookPriceFactor.objects.all().order_by('-factor', 'label')
    
    context = {
        'price_factors': price_factors,
        'total_count': price_factors.count(),
    }
    return render(request, 'dashboard/book_price_factors.html', context)