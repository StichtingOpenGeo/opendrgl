from djangular.views.crud import NgCRUDView

from data.models import TripPattern, Stop, TripPatternStop, Trip, Line
from utils.views import BaseNgView

# Custom views

class LineTripPatternView(BaseNgView):
    model = TripPattern
    query_slug = 'line'

    def get_data(self, param):
        return self.model.objects.filter(line_id=param, is_forward=(self.request.GET['is_forward'] == 'true'))

class TripPatternStopListView(BaseNgView):
    model = TripPatternStop
    query_slug = 'pattern'

    def get_data(self, param):
        return self.model.objects.order_by('order').filter(pattern_id=param)

class TripPatternTripView(BaseNgView):
    model = Trip
    query_slug = 'pattern'

    def get_data(self, param):
        return self.model.objects.filter(pattern_id=param)

# Default views

class StopView(NgCRUDView):
    model = Stop
    fields = ['agency', 'name']

class LineView(NgCRUDView):
    model = Line


class TripPatternView(NgCRUDView):
    model = TripPattern


class TripPatternStopView(NgCRUDView):
    model = TripPatternStop


class TripView(NgCRUDView):
    model = Trip
