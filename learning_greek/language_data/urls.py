from django.conf.urls import patterns, url


urlpatterns = patterns("learning_greek.language_data.views",
    url(r"^node/(\d{15})/$", "node_detail", name="node_detail"),
)
