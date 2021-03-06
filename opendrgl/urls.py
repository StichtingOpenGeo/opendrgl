import backbone
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
from projects.views import CreateProjectView, ProjectListView, ProjectPickView
from routes.views import RouteAppView
from stops.views import StopIndexView, StopCreateView, StopUpdateView

admin.autodiscover()
backbone.autodiscover()

urlpatterns = patterns('',
    url(r'^stops/?$', StopIndexView.as_view(), name='stop_index'),
    url(r'^stops/toevoegen/$', StopCreateView.as_view(), name='stop_add'),
    url(r'^stops/(?P<pk>\d+)/bewerk$', StopUpdateView.as_view(), name='stop_edit'),

    url(r'^projects/?$', ProjectListView.as_view(), name='project_list'),
    url(r'^projects/(?P<pk>\d+)$', ProjectPickView.as_view(), name='project_pick'),
    url(r'^project/add/?$', CreateProjectView.as_view(), name='project_add'),

    url(r'^routes/?$', RouteAppView.as_view(), name='routes_app'),

    url(r'^backbone/', include(backbone.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
