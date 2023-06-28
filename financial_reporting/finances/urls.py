from django.contrib import admin
from django.urls import path

from finances import views

app_name = 'finances'


urlpatterns = [
    path('', (views.index), name='index'),
    path('transactions/', views.transaction_list, name='transactions'),
    path('transactions/<str:transaction_type>', views.transaction_list, name='transactions_by_type'),
    path('transactions/<str:transaction_type>/<str:start_date>/<str:end_date>', views.transaction_list, name='transactions_by_period'),
    path('export', views.export_csv, name='export_csv'),
    path('import', views.import_csv, name='import_csv')
]
