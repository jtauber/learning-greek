from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User


ADOPTION_LEVEL_CHOICES = [
    ("bleeding-edge", "Bleeding Edge"),
    ("early-adopter", "Early Adopter"),
    ("mainstream", "Mainstream"),
]


class Preference(models.Model):
    
    user = models.OneToOneField(User)
    
    adoption_level = models.CharField(max_length=20, default="early-adopter", choices=ADOPTION_LEVEL_CHOICES)


def create_preferences(sender, instance, created, **kwargs):
    if created:
        Preference.objects.create(user=instance)


post_save.connect(create_preferences, sender=User)
