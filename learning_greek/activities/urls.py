from django.conf.urls import patterns, url

urlpatterns = patterns("learning_greek.activities.views",
    url(r"(?P<slug>\w+)/start/$", "activity_start", name="activity_start"),
    url(r"(?P<slug>\w+)/play/$", "activity_play", name="activity_play"),
)
