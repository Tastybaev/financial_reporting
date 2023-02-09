from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField('Хекскод цвета', max_length=255)
    slug = models.SlugField('Слаг', max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('tag', args=[self.slug])


class Transaction(models.Model):
    TRANSACTION_CHOICE = (
        ('income', 'Входящяя'),
        ('outgoing', 'Исходщяя')
    )
    transaction_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_id')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICE)
    currency = models.FloatField(max_length=20)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name='categories')
    slug = models.SlugField('Слаг', max_length=255)
    
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.description}'
