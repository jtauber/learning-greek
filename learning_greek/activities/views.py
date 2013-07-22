from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect

from account.decorators import login_required
from django.views.decorators.http import require_POST

from eventlog.models import log

from .models import ActivityState, get_activity_state, availability


@require_POST
@login_required
def activity_start(request, slug):
    
    Activity = settings.ACTIVITIES.get(slug)
    
    if Activity is None:
        raise Http404
    
    available, num_completions = availability(request.user, slug)
    if not available:
        log(
            user=request.user,
            action="ACTIVITY_ERROR",
            extra={
                "error": "not available",
                "slug": slug,
            }
        )
        # @@@ user message
        return redirect("dashboard")
    
    activity_state, _ = ActivityState.objects.get_or_create(user=request.user, activity_slug=slug)
    
    if activity_state.completed_count > 0 and not Activity.repeatable:
        log(
            user=request.user,
            action="ACTIVITY_ERROR",
            extra={
                "error": "not repeatable",
                "slug": slug,
            }
        )
        # @@@ user message
        return redirect("dashboard")
    
    return redirect("activity_play", slug)


@login_required
def activity_play(request, slug):
    
    Activity = settings.ACTIVITIES.get(slug)
    
    if Activity is None:
        raise Http404
    
    activity_state = get_activity_state(request.user, slug)
    
    if activity_state is None:
        log(
            user=request.user,
            action="ACTIVITY_ERROR",
            extra={
                "error": "not started",
                "slug": slug,
            }
        )
        # @@@ user message
        return redirect("dashboard")
    
    activity = Activity(activity_state.latest)
    
    return activity.handle_request(request)
