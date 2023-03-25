from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models

from .models import Category, Transaction


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    empty_value_display = '< Тут Пусто >'


class TrasactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'transaction_id',
        'transaction_type',
        'currency',
        'date',
        'description',
        'slug'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TrasactionAdmin)

# templates нужно сделать