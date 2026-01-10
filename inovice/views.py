from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from .models import Invoice
from book.models import BookLoan


@login_required
def payments_list_view(request):
    """View барои нишон додани рӯйхати пардохтҳо"""
    user_institution = request.user.institution
    
    if not user_institution:
        context = {
            'payments': [],
            'total_count': 0,
            'selected_status': '',
            'selected_class': '',
            'selected_group': '',
            'selected_payment_number': '',
            'selected_student': '',
            'date_from': '',
            'date_to': '',
        }
        return render(request, 'dashboard/payments_list.html', context)
    
    # Гирифтани ҳамаи пардохтҳо (invoices) барои муассисаи корбар
    invoices_queryset = Invoice.objects.filter(
        loan__institution=user_institution
    ).select_related('loan', 'loan__student', 'loan__book', 'loan__institution', 'loan__institution__region').order_by('-created_at')
    
    # Филтрҳо аз рӯи GET-параметрҳо
    status_filter = request.GET.get('status')
    class_filter = request.GET.get('class')
    group_filter = request.GET.get('group')
    payment_number_filter = request.GET.get('payment_number')
    student_filter = request.GET.get('student')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Филтри Статус
    if status_filter and status_filter != '':
        if status_filter == 'paid':
            invoices_queryset = invoices_queryset.filter(status=True)
        elif status_filter == 'unpaid':
            invoices_queryset = invoices_queryset.filter(status=False)
    
    # Филтри Синф
    if class_filter and class_filter != '':
        invoices_queryset = invoices_queryset.filter(loan__class_number=int(class_filter))
    
    # Филтри Гурӯҳ
    if group_filter and group_filter != '':
        invoices_queryset = invoices_queryset.filter(loan__student__class_latter__iexact=group_filter)
    
    # Филтри Рақами пардохт
    if payment_number_filter and payment_number_filter != '':
        try:
            # Интизор мешавем, ки рақам дода шавад
            payment_number = int(payment_number_filter)
            invoices_queryset = invoices_queryset.filter(invoice_code=payment_number)
        except (ValueError, TypeError):
            # Агар рақам набошад, ҷустуҷӯро иҷро намекунем
            pass
    
    # Филтри Хонанда
    if student_filter and student_filter != '':
        invoices_queryset = invoices_queryset.filter(loan__student__fullname__icontains=student_filter)
    
    # Филтри санаҳо
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            invoices_queryset = invoices_queryset.filter(created_at__date__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            invoices_queryset = invoices_queryset.filter(created_at__date__lte=date_to_obj)
        except ValueError:
            pass
    
    # Рӯйхати нотакрори синфҳо ва гурӯҳҳо барои филтр
    all_classes = Invoice.objects.filter(
        loan__institution=user_institution
    ).values_list('loan__class_number', flat=True).distinct().order_by('loan__class_number')
    
    all_groups = Invoice.objects.filter(
        loan__institution=user_institution
    ).values_list('loan__student__class_latter', flat=True).distinct()
    
    context = {
        'payments': invoices_queryset,
        'total_count': invoices_queryset.count(),
        'all_classes': sorted([c for c in all_classes if c]),
        'all_groups': sorted([g for g in all_groups if g]),
        'selected_status': status_filter or '',
        'selected_class': class_filter or '',
        'selected_group': group_filter or '',
        'selected_payment_number': payment_number_filter or '',
        'selected_student': student_filter or '',
        'date_from': date_from or '',
        'date_to': date_to or '',
    }
    return render(request, 'dashboard/payments_list.html', context)
