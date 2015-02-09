import django.dispatch


adoption_level_change = django.dispatch.Signal(providing_args=["level", "request"])
blurb_read = django.dispatch.Signal(providing_args=["request"])
