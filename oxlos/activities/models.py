from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import importlib, timezone

from django.contrib.auth.models import User

import jsonfield


class UserState(models.Model):
    """
    this stores the overall state of a particular user.
    """
    user = models.OneToOneField(User)
    
    data = jsonfield.JSONField()
    
    @classmethod
    def for_user(cls, user):
        user_state, _ = cls.objects.get_or_create(user=user)
        return user_state
    
    def get(self, key):
        return self.data.get(key)
    
    def set(self, key, value):
        self.data[key] = value
        self.save()


class ActivityState(models.Model):
    """
    this stores the overall state of a particular user doing a particular
    activity across all occurences of that activity.
    """
    
    user = models.ForeignKey(User)
    activity_slug = models.CharField(max_length=50)
    
    # how many occurences have been completed by this user
    completed_count = models.IntegerField(default=0)
    
    data = jsonfield.JSONField()
    
    class Meta:
        unique_together = [("user", "activity_slug")]
    
    @property
    def in_progress(self):
        try:
            return ActivityOccurrenceState.objects.get(
                user=self.user,
                activity_slug=self.activity_slug,
                completed=None
            )
        except ActivityOccurrenceState.DoesNotExist:
            return None
    
    @property
    def latest(self):
        occurrence, _ = ActivityOccurrenceState.objects.get_or_create(
            user=self.user,
            activity_slug=self.activity_slug,
            completed=None
        )
        return occurrence
    
    @property
    def last_completed(self):
        completed = ActivityOccurrenceState.objects.filter(
            user=self.user,
            activity_slug=self.activity_slug,
            completed__isnull=False
        ).order_by("-started")
        if completed:
            return completed[0]
        else:
            return None
    
    @property
    def all_occurrences(self):
        return ActivityOccurrenceState.objects.filter(
            user=self.user,
            activity_slug=self.activity_slug,
        ).order_by("started")


class ActivityOccurrenceState(models.Model):
    """
    this stores the state of a particular occurence of a particular user
    doing a particular activity.
    """
    
    user = models.ForeignKey(User)
    activity_slug = models.CharField(max_length=50)
    
    started = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(null=True)  # NULL means in progress
    
    data = jsonfield.JSONField()
    
    class Meta:
        unique_together = [("user", "activity_slug", "started")]
    
    def mark_completed(self):
        self.completed = timezone.now()
        self.save()
        activity_state = ActivityState.objects.get(
            user=self.user,
            activity_slug=self.activity_slug
        )
        activity_state.completed_count = models.F("completed_count") + 1
        activity_state.save()


def get_activity_state(user, activity_slug):
    
    try:
        activity_state = ActivityState.objects.get(user=user, activity_slug=activity_slug)
    except ActivityState.DoesNotExist:
        activity_state = None
    
    return activity_state


def availability(user, activity_slug):
    
    adoption_level = user.preference.adoption_level
    
    # number of people who have completed this at least once
    num_completions = ActivityState.objects.filter(
        activity_slug=activity_slug
    ).exclude(
        completed_count=0
    ).count()

    if adoption_level == "bleeding-edge":
        available = True
    elif adoption_level == "early-adopter" and num_completions >= 10:
        available = True
    elif adoption_level == "maintream" and num_completions >= 100:
        available = True
    else:
        available = False
    
    return available, num_completions


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i+1:]
    try:
        mod = importlib.import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured("Error importing %s: '%s'" % (module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '%s' does not define a '%s'" % (module, attr))
    return attr


def get_activities(user):
    
    activities = {
        "available": [],
        "inprogress": [],
        "completed": [],
        "repeatable": [],
        "unavailable": [],
    }
    
    for slug, activity_class_path in settings.ACTIVITIES.items():
        activity = load_path_attr(activity_class_path)
        state = get_activity_state(user, slug)
        user_num_completions = ActivityOccurrenceState.objects.filter(
            user=user,
            activity_slug=slug,
            completed__isnull=False
        ).count()
        activity_entry = {
            "slug": slug,
            "title": activity.title,
            "description": activity.description,
            "state": state,
            "user_num_completions": user_num_completions,
            "repeatable": activity.repeatable,
        }
        if state:
            if state.in_progress:
                activities["inprogress"].append(activity_entry)
            elif activity.repeatable:
                activities["repeatable"].append(activity_entry)
            else:
                activities["completed"].append(activity_entry)
        else:
            available, num_completions = availability(user, slug)
            if available:
                activities["available"].append(activity_entry)
            else:
                activity_entry["unavailable"] = True
                activity_entry["num_completions"] = num_completions
                activities["unavailable"].append(activity_entry)
    
    return activities
