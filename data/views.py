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

class DefaultCRUDView(LoginRequiredMixin, NgCRUDView):

    def get_user_agency(self):
        if self.request.user.profile:
            return self.request.user.profile.default_agency.pk
        return None


class StopView(DefaultCRUDView):
    model = Stop
    fields = ['agency', 'name', 'lat', 'lon']

    def get_form_kwargs(self):
        kwargs = super(StopView, self).get_form_kwargs();
        kwargs['data']['agency'] = self.get_user_agency()
        return kwargs

    def get_queryset(self):
        return super(StopView, self).get_queryset().filter(agency=self.get_user_agency())


class LineView(DefaultCRUDView):
    model = Line

    def get_form_kwargs(self):
        kwargs = super(LineView, self).get_form_kwargs();
        kwargs['data']['agency'] = self.get_user_agency()
        return kwargs

    def get_queryset(self):
        return super(LineView, self).get_queryset().filter(agency=self.get_user_agency())


class TripPatternView(DefaultCRUDView):
    model = TripPattern

    def get_queryset(self):
        return super(TripPatternView, self).get_queryset().filter(line__agency=self.get_user_agency())


class TripPatternStopView(DefaultCRUDView):
    model = TripPatternStop

    def get_queryset(self):
        return super(TripPatternStopView, self).get_queryset().filter(pattern__line__agency=self.get_user_agency())


class TripView(DefaultCRUDView):
    model = Trip

    def get_queryset(self):
        return super(TripView, self).get_queryset().filter(pattern__line__agency=self.get_user_agency())
