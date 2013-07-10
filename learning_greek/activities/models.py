from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

import jsonfield


class ActivityState(models.Model):
    
    user = models.ForeignKey(User)
    activity_slug = models.CharField(max_length=50)
    
    started = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(null=True)  # NULL means in progress
    
    data = jsonfield.JSONField()
    
    class Meta:
        # @@@ initially assume an activity is only done once per user
        unique_together = [("user", "activity_slug")]


def get_activity_state(user, activity_slug):
    
    try:
        activity_state = ActivityState.objects.get(user=user, activity_slug=activity_slug)
    except ActivityState.DoesNotExist:
        activity_state = None
    
    return activity_state


def get_activities(user):
    
    activities = {
        "available": [],
        "inprogress": [],
        "completed": [],
        "unavailable": [],
    }
    
    for slug, activity in settings.ACTIVITIES.items():
        state = get_activity_state(user, slug)
        activity_entry = {
            "slug": slug,
            "title": activity.title,
            "description": activity.description,
            "help_text": getattr(activity, "help_text", ""),
            "state": state,
        }
        if state:
            if state.completed:
                activities["completed"].append(activity_entry)
            else:
                activities["inprogress"].append(activity_entry)
        else:
            activities["available"].append(activity_entry)
    
    return activities
