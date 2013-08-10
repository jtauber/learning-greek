from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from django.contrib.auth.models import User

from account.decorators import login_required

from oxlos.activities.models import load_path_attr, ActivityOccurrenceState, ActivityState


@login_required
def staff_dashboard(request):
    
    if not request.user.is_staff:
        raise Http404
    
    activities = []
    
    for slug, activity_class_path in settings.ACTIVITIES.items():
        activity = load_path_attr(activity_class_path)
        activity_states = ActivityState.objects.filter(activity_slug=slug)
        completed_activity_states = activity_states.exclude(completed_count=0)
        activity_occurrence_states = ActivityOccurrenceState.objects.filter(activity_slug=slug)
        completed_activity_occurrence_states = activity_occurrence_states.filter(completed__isnull=False)
        
        activities.append({
            "slug": slug,
            "title": activity.title,
            "activity_states": activity_states,
            "completed_activity_states": completed_activity_states,
            "activity_occurrence_states": activity_occurrence_states,
            "completed_activity_occurrence_states": completed_activity_occurrence_states,
        })
    return render(request, "staff/dashboard.html", {
        "users": User.objects.all(),
        "activity_states": ActivityState.objects.all(),
        "activity_occurrence_states": ActivityOccurrenceState.objects.all(),
        "activities": activities,
    })


@login_required
def staff_activity_detail(request, slug):
    
    if not request.user.is_staff:
        raise Http404
    
    activity_states = ActivityState.objects.filter(activity_slug=slug)
    activity_occurrence_states = ActivityOccurrenceState.objects.filter(activity_slug=slug)
    
    return render(request, "staff/activity_detail.html", {
        "activity_states": activity_states,
        "activity_occurrence_states": activity_occurrence_states,
    })
