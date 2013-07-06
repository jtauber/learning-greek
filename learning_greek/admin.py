from django.contrib import admin

from learning_greek.models import Preference


admin.site.register(Preference, list_display=["user", "adoption_level"])
