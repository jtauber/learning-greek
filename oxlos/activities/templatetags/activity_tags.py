from django import template

register = template.Library()


@register.assignment_tag
def get_user_stats_for(user):
    event_count = user.log_set.count()
    if event_count:
        last_event = user.log_set.order_by("-timestamp")[0].timestamp
    else:
        last_event = None
    return {
        "username": user.username,
        "events": event_count,
        "last_event": last_event,
        "adoption_level": user.preference.adoption_level,
        "activities": user.activitystate_set.count(),
        "occurrences": user.activityoccurrencestate_set.count(),
        "completed_occurrences": user.activityoccurrencestate_set.filter(completed__isnull=False).count(),
    }
