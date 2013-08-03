import django.dispatch


activity_start = django.dispatch.Signal(providing_args=["slug", "activity_state", "request"])
activity_play = django.dispatch.Signal(providing_args=["slug", "activity_occurrence_state", "request"])
activity_completed = django.dispatch.Signal(providing_args=["slug", "activity_occurrence_state", "request"])
