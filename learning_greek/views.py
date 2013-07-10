from django.shortcuts import redirect, render

from account.decorators import login_required
from account.views import SettingsView as AccountSettingsView

from learning_greek.forms import SettingsForm
from learning_greek.activities.models import get_activities


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


def home(request):
    
    if request.user.is_authenticated():
        return redirect("dashboard")
    
    return render(request, "homepage.html")


@login_required
def dashboard(request):
    
    return render(request, "dashboard.html", {
        "activities": get_activities(request.user),
    })
