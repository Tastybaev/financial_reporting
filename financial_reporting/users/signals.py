from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from finances.models import Category


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        default_categories = ['Еда', 'Транспорт', 'Одежда', 'Косметика', 'Супермаркет', 'Медицина', 'Образование', 'Прочие']
        for category in default_categories:
            Category.objects.create(owner=instance, name=category)

