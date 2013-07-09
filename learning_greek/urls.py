from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


from learning_greek.views import SettingsView


urlpatterns = patterns("",
    url(r"^$", "learning_greek.views.home", name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/settings/$", SettingsView.as_view(), name="account_settings"),
    url(r"^account/", include("account.urls")),
    
    url(r"^activity/", include("learning_greek.activities.urls")),
    
    url(r"^dashboard/", "learning_greek.views.dashboard", name="dashboard"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
