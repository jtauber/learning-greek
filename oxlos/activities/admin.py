
from django.contrib import admin

from .models import UserState, ActivityState, ActivityOccurrenceState


admin.site.register(UserState, list_display=["user", "data"])
admin.site.register(ActivityState, list_display=["activity_slug", "user", "data"])
admin.site.register(ActivityOccurrenceState, list_display=["activity_slug", "user", "started", "completed", "data"])
