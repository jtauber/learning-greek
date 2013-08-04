from django import template

register = template.Library()


@register.assignment_tag
def get_user_stats_for(user):
    return {
        "username": user.username,
        "events": user.log_set.count(),
        "adoption_level": user.preference.adoption_level,
        "activities": user.activitystate_set.count(),
        "occurrences": user.activityoccurrencestate_set.count(),
        "completed_occurrences": user.activityoccurrencestate_set.filter(completed__isnull=False).count(),
    }
