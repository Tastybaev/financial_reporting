from django.forms import ModelForm, ValidationError
from .models import Transaction, TransactionImport, Category


class AddTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = (
            'transaction_type', 
            'currency',
            'description',
            'category',
        )
    
    def __init__(self, user, *args, **kwargs):
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=user)

    def clean_currency(self):
        currency = self.cleaned_data['currency']
        if currency < 0:
            raise ValidationError('Сумма не может быть отрицательной!')
        return currency

class TransactionsImportForm(ModelForm):
    class Meta:
        model = TransactionImport
        fields = ('csv_file',)

# сделать юзера.