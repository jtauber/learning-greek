from django.contrib import admin

from .models import Preference


admin.site.register(Preference, list_display=["user", "adoption_level"])
