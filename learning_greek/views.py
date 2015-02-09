from account.views import SettingsView as AccountSettingsView

from .forms import SettingsForm
from .signals import adoption_level_change


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
