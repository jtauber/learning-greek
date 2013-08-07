from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect

from account.decorators import login_required
from django.views.decorators.http import require_POST

from eventlog.models import log

from .models import ActivityState, get_activity_state, availability, load_path_attr
from .signals import activity_start as activity_start_signal, activity_play as activity_play_signal, activity_completed as activity_completed_signal


@require_POST
@login_required
def activity_start(request, slug):
    
    activity_class_path = settings.ACTIVITIES.get(slug)
    
    if activity_class_path is None:
        raise Http404
    
    Activity = load_path_attr(activity_class_path)
    
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
    
    activity_start_signal.send(sender=request.user, slug=slug, activity_state=activity_state, request=request)
    return redirect("activity_play", slug)


@login_required
def activity_play(request, slug):
    
    activity_class_path = settings.ACTIVITIES.get(slug)
    
    if activity_class_path is None:
        raise Http404
    
    Activity = load_path_attr(activity_class_path)
    
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
    
    activity = Activity(activity_state.latest, activity_state)
    
    activity_play_signal.send(sender=request.user, slug=slug, activity_occurrence_state=activity_state.latest, request=request)
    return activity.handle_request(request)


@login_required
def activity_completed(request, slug):

    activity_class_path = settings.ACTIVITIES.get(slug)
    
    if activity_class_path is None:
        raise Http404
    
    Activity = load_path_attr(activity_class_path)
    
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
    
    last_completed = activity_state.last_completed
    
    if last_completed is None:
        log(
            user=request.user,
            action="ACTIVITY_ERROR",
            extra={
                "error": "not completed",
                "slug": slug,
            }
        )
        # @@@ user message
        return redirect("dashboard")
    
    activity = Activity(last_completed, activity_state)
    
    activity_completed_signal.send(sender=request.user, slug=slug, activity_occurrence_state=last_completed, request=request)
    
    return activity.completed(request)
