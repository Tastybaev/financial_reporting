# Generated by Django 4.1.5 on 2023-05-15 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0007_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='transaction',
            constraint=models.CheckConstraint(check=models.Q(('transaction_type__in', ['income', 'outgoing'])), name='finances_transaction_transaction_type_valid'),
        ),
    ]
