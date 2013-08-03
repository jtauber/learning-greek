from django.conf.urls import patterns, url


urlpatterns = patterns("learning_greek.staff.views",
    url(r"^$", "staff_dashboard", name="staff_dashboard"),
)
