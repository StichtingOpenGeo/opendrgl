from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from djangular.views.crud import NgCRUDView

from data.models import TripPattern, Stop, TripPatternStop, Trip, Line

###
# Index
###
class IndexView(LoginRequiredMixin, TemplateView):
    template_name="app.html"

###
# Angular Views
###

class StopView(NgCRUDView):
    model = Stop
    fields = ['agency', 'name', 'lat', 'lon']

class LineView(NgCRUDView):
    model = Line


class TripPatternView(NgCRUDView):
    model = TripPattern


class TripPatternStopView(NgCRUDView):
    model = TripPatternStop


class TripView(NgCRUDView):
    model = Trip
