from django.contrib import admin
from django.urls import path

from finances import views


urlpatterns = [
    path('', (views.index), name='index'),
    path('transactions/', views.transaction_list, name='transactions'),
]
