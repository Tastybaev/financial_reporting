# Generated by Django 4.1.5 on 2023-05-24 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0010_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['date'], 'verbose_name': 'Транзакция', 'verbose_name_plural': 'Транзакции'},
        ),
    ]
