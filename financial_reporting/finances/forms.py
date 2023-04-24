from django.forms import ModelForm
from .models import Transaction


class AddTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = (
            'transaction_type', 
            'currency',
            'description',
            'category',
        )
