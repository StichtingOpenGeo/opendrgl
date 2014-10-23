from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import DetailView
from djangular.views.crud import NgCRUDView
from data.models import TripPattern, Stop, TripPatternStop, Trip, Line


class LineOverviewView(NgCRUDView, DetailView):
    model = Line

    def dispatch(self, request, *args, **kwargs):
        return self.build_json_response(self.get_queryset())

    def get_object(self, queryset=None):
        if 'pk' in self.request.GET:
            try:
                return self.model.objects.get(pk=self.request.GET['pk'])
            except ObjectDoesNotExist:
                raise Http404
        else:
            raise Http404

class StopView(NgCRUDView):
    model = Stop

class TripPatternView(NgCRUDView):
    model = TripPattern

class TripPatternStopView(NgCRUDView):
    model = TripPatternStop

class TripView(NgCRUDView):
    model = Trip
