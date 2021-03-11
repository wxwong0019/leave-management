from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .model import Profile

def create_profile(sender, instance, created, **kwarg):
	if created:
		Profile.objects.create(user=instance)

def save_profile(sender, instance, **kwarg):
	instance.profile.save()