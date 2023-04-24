from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView

import json

from .forms import AddTransactionForm
from .models import Transaction


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
def transaction_list(request, transaction_type=None):
    print(transaction_type)
    data_income = [{
        'date_income': obj.date.isoformat(timespec='minutes'),
        'value_income': obj.currency
    }
    for obj in Transaction.objects.filter(transaction_id=request.user, transaction_type='income')]
    data_outgoing = [{
        'date_outgoing': obj.date.isoformat(timespec='minutes'),
        'value_outgoing': obj.currency
    }
    for obj in Transaction.objects.filter(transaction_id=request.user, transaction_type='outgoing')]
    dump_in = json.dumps(data_income)
    dump_out = json.dumps(data_outgoing)
    if transaction_type:
        transactions = Transaction.objects.filter(transaction_id=request.user, transaction_type=transaction_type)
    else:
        transactions = Transaction.objects.filter(transaction_id=request.user)
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
        'dump_in': dump_in,
        'dump_out': dump_out,
        'add_transaction_form': add_transaction_form,
        'page_number': page_number
    }
    return render(request, "finances/transactions.html", context)


# @login_required
# def transaction_income(request):
#     data_income = [{
#         'date_income': obj.date.isoformat(timespec='minutes'),
#         'value_income': obj.currency
#     }
#     for obj in Transaction.objects.filter(transaction_id=request.user, transaction_type='income')]
#     dump_in = json.dumps(data_income)
#     transactions = Transaction.objects.filter(transaction_id=request.user, transaction_type='income')
#     paginator = Paginator(transactions, 20)
#     page_number = request.GET.get('page_number')
