from djangular.views.crud import NgCRUDView

from data.models import TripPattern, Stop, TripPatternStop, Trip, Line

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
