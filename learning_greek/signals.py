import django.dispatch


adoption_level_change = django.dispatch.Signal(providing_args=["level", "request"])
