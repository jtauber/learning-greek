from django import forms

from account.forms import SettingsForm as AccountSettingsForm

from learning_greek.models import ADOPTION_LEVEL_CHOICES

ADOPTION_LEVEL_HELP_TEXT = """
<b>Adoption level</b> determines when a new survey or game will be made available to you.
<small>
If you want access as soon as it&rsquo;s launched, select <b>Bleeding Edge</b>.
If you want to wait until <i>at least 10 other people</i> have tried it, select <b>Early Adopter</b>.
If you want to wait until <i>at least 100 other people</i> have tried it, select <b>Mainstream</b>.
</small>
"""


class SettingsForm(AccountSettingsForm):
    
    adoption_level = forms.ChoiceField(choices=ADOPTION_LEVEL_CHOICES, help_text=ADOPTION_LEVEL_HELP_TEXT)
