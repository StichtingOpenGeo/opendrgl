from django.conf.urls import patterns, url
from chb.views import StopSearchView

__author__ = 'Joel Haasnoot'

urlpatterns = patterns('',
    url(r'^data/chb/?$', StopSearchView.as_view(), name='chbstop_crud')

)