from django.contrib.auth.decorators import user_passes_test

def can_import_csv(user):
    return user.groups.filter(name='Premium').exists()

def cannot_import_csv(user):
    return not user.groups.filter(name='Standart').exists()

premium_required = user_passes_test(can_import_csv, login_url='users:pricing')
standart_required = user_passes_test(cannot_import_csv, login_url='users:pricing')