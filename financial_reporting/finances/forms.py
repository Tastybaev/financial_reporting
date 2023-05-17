from django.forms import ModelForm
from .models import Transaction, TransactionImport


class AddTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = (
            'transaction_type', 
            'currency',
            'description',
            'category',
        )

class TransactionsImportForm(ModelForm):
    class Meta:
        model = TransactionImport
        fields = ('csv_file',)
