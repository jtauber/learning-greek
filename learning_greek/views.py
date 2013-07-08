from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from account.decorators import login_required
from account.views import SettingsView as AccountSettingsView

from learning_greek.activities import ACTIVITIES
from learning_greek.forms import SettingsForm
from learning_greek.models import ActivityState


class SettingsView(AccountSettingsView):
    
    form_class = SettingsForm
    
    def get_initial(self):
        initial = super(SettingsView, self).get_initial()
        initial["adoption_level"] = self.request.user.preference.adoption_level
        return initial
    
    def form_valid(self, form):
        preference = self.request.user.preference
        preference.adoption_level = form.cleaned_data["adoption_level"]
        preference.save()
        return super(SettingsView, self).form_valid(form)


@login_required
def dashboard(request):
    # faked
    activities = [
        {
            "slug": "demographic",
            "title": "Demographic Survey",
            "description": "basic demographic questions",
        }
    ]
    
    for activity in activities:
        try:
            activity_state = ActivityState.objects.get(user=request.user, activity_slug=activity["slug"])
            activity.update({"state": activity_state})
        except ActivityState.DoesNotExist:
            activity.update({"state": None})
    
    return render(request, "dashboard.html", {
        "activities": activities,
    })


# @@@ should we just get rid of this and merge with "play"?
@require_POST
@login_required
def activity_start(request, slug):
    ActivityState.objects.get_or_create(user=request.user, activity_slug=slug)
    return redirect("activity_play", slug)


@login_required
def activity_play(request, slug):
    Activity = ACTIVITIES.get(slug)
    if Activity is None:
        raise Http404
    try:
        activity_state = ActivityState.objects.get(user=request.user, activity_slug=slug)
    except ActivityState.DoesNotExist:
        # @@@ error message?
        return redirect("dashboard")
    activity = Activity(activity_state.state)
    return activity.handle_request(request)
