from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from datetime import datetime

import csv
import json

from .decorators import premium_required, standart_required
from .forms import AddTransactionForm, TransactionsImportForm
from .models import Transaction, Category


def index(request):
    templates = 'finances/index.html'
    text = 'Это главная страница проекта financial_reporting'
    context = {
        'text': text,
    }
    return render(request, templates, context)


@login_required
def profile(request, user):
    user = get_object_or_404(User, user=user)
    context = {
        'user': user,
        'profile': user,
    }
    return render(request, "finances/profile.html", context)


@login_required
def transaction_list(request, transaction_type=None, start_date=None, end_date=None):
    data = [{
            'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'value': 0
        }
        ]
    dump = json.dumps(data[::-1])
    print(transaction_type, start_date, end_date)
    if transaction_type == 'null' and start_date and end_date:
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        end_date = datetime.strptime(end_date, '%d.%m.%Y')
        transactions = Transaction.objects.filter(transaction_id=request.user, date__range=(start_date, end_date))
        currency_sum = transactions.aggregate(currency_sum=Sum('currency'))['currency_sum']
    elif transaction_type and start_date and end_date:
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        end_date = datetime.strptime(end_date, '%d.%m.%Y')
        data = [{
            'date': obj.date.strftime('%d.%m.%Y %H:%M'),
            'value': obj.currency
        }
        for obj in Transaction.objects.filter(transaction_id=request.user, transaction_type=transaction_type, date__range=(start_date, end_date))]
        dump = json.dumps(data[::-1])
        transactions = Transaction.objects.filter(transaction_id=request.user, transaction_type=transaction_type, date__range=(start_date, end_date))
        currency_sum = transactions.aggregate(currency_sum=Sum('currency'))['currency_sum']
    elif transaction_type:
        data = [{
            'date': obj.date.strftime('%d.%m.%Y %H:%M'),
            'value': obj.currency
        }
        for obj in Transaction.objects.filter(transaction_id=request.user, transaction_type=transaction_type)]
        dump = json.dumps(data[::-1])
        transactions = Transaction.objects.filter(transaction_id=request.user, transaction_type=transaction_type)
        currency_sum = transactions.aggregate(currency_sum=Sum('currency'))['currency_sum']
    else:
        transactions = Transaction.objects.filter(transaction_id=request.user)
        currency_sum = transactions.aggregate(currency_sum=Sum('currency'))['currency_sum']
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page_number')
    try:
        transactions_paginator = paginator.page(page_number)
    except PageNotAnInteger:    
        transactions_paginator = paginator.page(1)
    except EmptyPage:
        transactions_paginator = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        add_transaction_form = AddTransactionForm(data=request.POST)
        if add_transaction_form.is_valid():
            new_transaction = add_transaction_form.save(commit=False)
            new_transaction.transaction_id = request.user
            new_transaction.save()
            return redirect(request.path)
    else:
        add_transaction_form = AddTransactionForm()
    context = {
        'transactions': transactions_paginator,
        'dump': dump,
        'add_transaction_form': add_transaction_form,
        'page_number': page_number,
        'currency_sum': currency_sum
    }
    return render(request, "finances/transactions.html", context)


@login_required
def delete_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(pk=transaction_id)
    except Transaction.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Транзакция не найдена.'}, status=404)
    # Удалите транзакцию
    transaction.delete()
    return JsonResponse({'success': True, 'message': 'Транзакция успешно удалена.'})


@login_required
def export_csv(request):
    transactions = Transaction.objects.filter(transaction_id=request.user)
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="transactions.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["id", "Тип транзакции", "Сумма", "Дата", "Описание", "Категория"])
    transactions_value_list = []
    for transaction in transactions:
        transactions_value_list.append((
            transaction.id,
            transaction.get_transaction_type_display(),
            transaction.currency,
            transaction.date.strftime('%d.%m.%Y %H:%M'),
            transaction.description,
            transaction.category.name
        ))
    for tvl in transactions_value_list:
        writer.writerow(tvl)
    return response


@login_required
@premium_required
def import_csv(request):
    if request.method == 'POST':
        form = TransactionsImportForm(request.POST, request.FILES)
        if form.is_valid():
            # сохраняем загруженный файл и делаем запись в базу
            form_object = form.save()
            # обработка csv файла
            with form_object.csv_file.open('r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                if next(rows) != ['id', 'Тип транзакции', 'Сумма', 'Дата', 'Описание', 'Категория']:
                    # обновляем страницу пользователя
                    # с информацией о какой-то ошибке
                    # messages.warning(request, 'Неверные заголовки у файла')
                    HttpResponse('Неверные заголовки у файла.')
                    return HttpResponseRedirect(request.path_info)
                for row in rows:
                    print(row[2])
                    # добавляем данные в базу
                    category_name = row[4]
                    category, _ = Category.objects.get_or_create(name=category_name)
                    type = ''
                    if row[1] == 'Входящая':
                        type = 'income'
                    elif row[1] == 'Исходящая':
                        type = 'outgoing'
                    else:
                        type = row[1]
                    transaction = Transaction(
                        transaction_id=request.user,
                        transaction_type=type,
                        currency=row[2],
                        date=datetime.strptime(row[3], '%d.%m.%Y %H:%M'),
                        description=row[4],
                        category=category
                    )
                    transaction.save()
            url = reverse('finances:transactions')
            # messages.success(request, 'Файл успешно импортирован')
            HttpResponse('Файл успешно импортирован.')
            return HttpResponseRedirect(url)
    form = TransactionsImportForm()
    return render(request, 'includes/csv_import.html', {'form': form})

