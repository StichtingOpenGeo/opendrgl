from django.conf.urls import patterns, include, url
from django.contrib import admin
from data.rest import router
from data.views import TripPatternView, TripPatternStopView, StopView, TripView, LineView, IndexView

urlpatterns = patterns('',

    url(r'', include('chb.urls')),
    url(r'^', include(router.urls)),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name="app_login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="app_logout"),
    url(r'^password/change', 'django.contrib.auth.views.password_change', {'template_name': 'users/password_change_form.html'}, name="app_password_change"),
    url(r'^password/changed', 'django.contrib.auth.views.password_change_done', {'template_name': 'users/password_change_done.html'}, name="app_password_changed"),

    url(r'^data/line/?$', LineView.as_view(), name='line_detail'),
    url(r'^data/stop/?$', StopView.as_view(), name='stop_crud'),
    url(r'^data/trip_pattern/?$', TripPatternView.as_view(), name='trip_pattern_crud'),
    url(r'^data/trip_pattern_stop/?$', TripPatternStopView.as_view(), name='trip_pattern_stop_crud'),
    url(r'^data/trip/?$', TripView.as_view(), name='trip_crud'),


    url(r'^admin/', include(admin.site.urls))
)
