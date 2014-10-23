from django.conf.urls import patterns, include, url
from django.contrib import admin
from data.views import TripPatternView, TripPatternStopView, StopView, TripView, LineOverviewView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opendrgl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^data/line/?$', LineOverviewView.as_view(), name='line_detail'),
    url(r'^data/stop/?$', StopView.as_view(), name='stop_crud'),
    url(r'^data/trip_pattern/?$', TripPatternView.as_view(), name='trip_pattern_crud'),
    url(r'^data/trip_pattern_stop/?$', TripPatternStopView.as_view(), name='trip_pattern_stop_crud'),
    url(r'^data/trip/?$', TripView.as_view(), name='trip_crud'),

    url(r'^admin/', include(admin.site.urls))
)
