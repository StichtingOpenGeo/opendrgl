from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.http import Http404
from django.views.generic import DetailView
from djangular.views.crud import NgCRUDView
from data.models import TripPattern, Stop, TripPatternStop, Trip, Line

class BaseNgView(NgCRUDView, DetailView):
    query_slug = None

    def dispatch(self, request, *args, **kwargs):
        if self.query_slug is None:
            raise ImproperlyConfigured("No query slug")
        if self.query_slug not in self.request.GET:
            raise Http404
        try:
            obj = self.get_object(self.request.GET[self.query_slug])
            return self.build_json_response(self.get_object(obj))
        except ObjectDoesNotExist:
            raise Http404


class LineTripPatternView(BaseNgView):
    model = TripPattern
    query_slug = 'line'

    def get_object(self, param, queryset=None):
        return self.model.objects.filter(line_id=param, is_forward=(self.request.GET['is_forward'] == 'true'))

class TripPatternStopListView(BaseNgView):
    model = TripPatternStop
    query_slug = 'pattern'

    def get_object(self, param, queryset=None):
        return self.model.objects.select_related('stop').filter(pattern_id=param)

class TripPatternTripView(NgCRUDView, DetailView):
    model = Trip
    query_slug = 'pattern'

    def get_object(self, param, queryset=None):
        return self.model.objects.filter(pattern_id=self.request.GET['pattern'])

class StopView(NgCRUDView):
    model = Stop

class LineView(NgCRUDView):
    model = Line

class TripPatternView(NgCRUDView):
    model = TripPattern

class TripPatternStopView(NgCRUDView):
    model = TripPatternStop

class TripView(NgCRUDView):
    model = Trip
