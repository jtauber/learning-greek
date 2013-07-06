from account.views import SettingsView as AccountSettingsView

from learning_greek.forms import SettingsForm


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
