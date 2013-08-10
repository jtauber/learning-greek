from django.conf.urls import patterns, url


urlpatterns = patterns("oxlos.staff.views",
    url(r"^$", "staff_dashboard", name="staff_dashboard"),
)
