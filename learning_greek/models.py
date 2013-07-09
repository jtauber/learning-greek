from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from django.contrib.auth.models import User

import jsonfield


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


class ActivityState(models.Model):
    
    user = models.ForeignKey(User)
    activity_slug = models.CharField(max_length=50)
    
    started = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(null=True)  # NULL means in progress
    
    state = jsonfield.JSONField()
    
    class Meta:
        # @@@ initially assume an activity is only done once per user
        unique_together = [("user", "activity_slug")]


def get_activity_state(user, activity_slug):
    try:
        activity_state = ActivityState.objects.get(user=user, activity_slug=activity_slug)
    except ActivityState.DoesNotExist:
        activity_state = None
    
    return activity_state
