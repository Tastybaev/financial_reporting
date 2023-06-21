from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=get_user_model())
def set_default_group(sender, instance, created, **kwargs):
    if created:
        default_group = Group.objects.get(name='Standart')  # Получаем группу "standart"
        instance.groups.add(default_group)  # Добавляем пользователя в группу по умолчанию