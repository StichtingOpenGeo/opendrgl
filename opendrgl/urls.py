from django.conf.urls import patterns, include, url

from django.contrib import admin
from stops.views import StopIndexView, StopCreateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^stops/?$', StopIndexView.as_view(), name='stop_index'),
    url(r'^stops/add/$', StopCreateView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
)
