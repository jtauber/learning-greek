from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect

from account.decorators import login_required
from django.views.decorators.http import require_POST

from .models import ActivityState, get_activity_state, availability


@require_POST
@login_required
def activity_start(request, slug):
    
    Activity = settings.ACTIVITIES.get(slug)
    
    if Activity is None:
        raise Http404
    
    available, num_completions = availability(request.user, slug)
    if not available:
        # @@@ error message?
        return redirect("dashboard")
    
    activity_state, _ = ActivityState.objects.get_or_create(user=request.user, activity_slug=slug)
    
    return redirect("activity_play", slug)


@login_required
def activity_play(request, slug):
    
    Activity = settings.ACTIVITIES.get(slug)
    
    if Activity is None:
        raise Http404
    
    activity_state = get_activity_state(request.user, slug)
    
    if activity_state is None:
        # @@@ error message?
        return redirect("dashboard")
    
    activity = Activity(activity_state.latest)
    
    return activity.handle_request(request)
