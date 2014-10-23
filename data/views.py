from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import DetailView
from djangular.views.crud import NgCRUDView
from data.models import TripPattern, Stop, TripPatternStop, Trip, Line


class TripPatternOverviewView(NgCRUDView, DetailView):
    model = TripPattern
    filter = ['pk']

    def dispatch(self, request, *args, **kwargs):
        qry = self.get_object()
        return self.build_json_response(qry)

    def get_object(self, queryset=None):
        if 'pk' in self.request.GET:
            try:
                return self.model.objects.filter(line_id=self.request.GET['pk'])
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
