from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import (
    MyUser, StatusModel, Profil
)

@receiver(post_save, sender = MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created :
        Profil.objects.create(user = instance, status = StatusModel.objects.first(), user_create = instance)