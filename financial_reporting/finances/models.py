from django.contrib.auth import get_user_model
from django.db import models

from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='owner')
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', args=[self.slug])


class TransactionType(models.TextChoices):
    INCOME = 'income', 'Входящая'
    OUTGOING = 'outgoing', 'Исходящая'

class Transaction(models.Model):
    transaction_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_id')
    transaction_type = models.CharField('Тип транзакции', max_length=10, choices=TransactionType.choices)
    currency = models.FloatField('Сумма', max_length=20)
    date = models.DateTimeField('Дата', default=timezone.now)
    description = models.TextField('Описание')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, related_name='categories', verbose_name='Категория')
    
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date']
        constraints = [
            models.CheckConstraint(
            name="%(app_label)s_%(class)s_transaction_type_valid",
            check=models.Q(transaction_type__in=TransactionType.values)
            )
        ]

    def __str__(self):
        return f'{TransactionType(self.transaction_type).label}'
    
    def save(self, *args, **kwargs):
        if self.transaction_type == 'income':
            self.currency = +abs(self.currency)
        elif self.transaction_type == 'outgoing':
            self.currency = -abs(self.currency)
        super().save(*args, **kwargs)
    
    def get_currency_display(self) -> str:
        if self.transaction_type == 'income':
            return f'+{self.currency}'
        return str(self.currency)

class TransactionImport(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
    date_added = models.DateTimeField(auto_now_add=True)