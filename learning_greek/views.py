from django.shortcuts import redirect, render

from account.decorators import login_required
from account.views import SettingsView as AccountSettingsView

from pinax.lms.activities.models import get_activities, UserState

from .forms import SettingsForm
from .signals import adoption_level_change, blurb_read


class SettingsView(AccountSettingsView):

    form_class = SettingsForm

    def get_initial(self):

        initial = super(SettingsView, self).get_initial()
        initial["adoption_level"] = self.request.user.preference.adoption_level

        return initial

    def form_valid(self, form):

        preference = self.request.user.preference
        previous_level = preference.adoption_level
        preference.adoption_level = form.cleaned_data["adoption_level"]
        preference.save()

        if preference.adoption_level != previous_level:
            adoption_level_change.send(sender=self.request.user, level=preference.adoption_level, request=self.request)

        return super(SettingsView, self).form_valid(form)


def home(request):
    if request.user.is_authenticated():
        return redirect("dashboard")
    return render(request, "homepage.html")


@login_required
def dashboard(request):

    user_state = UserState.for_user(request.user)
    # @@@ would be nice to generalize this
    if not user_state.get("intro_dashboard_blurb"):
        if request.method == "POST" and "read_blurb" in request.POST:
            user_state.set("intro_dashboard_blurb", True)
            blurb_read.send(sender=request.user, request=request)
            return redirect("dashboard")
        else:
            return render(request, "intro_dashboard_blurb.html")

    debug_mode = (request.GET.get("debug") is not None) and request.user.is_staff
    activities = get_activities(request.user)

    return render(request, "dashboard.html", {
        "debug_mode": debug_mode,
        "activities": activities,
    })
