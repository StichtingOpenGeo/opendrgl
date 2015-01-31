from rest_framework import routers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from data.models import Line, TripPattern, Calendar
from data.serializers import TripPatternStopSerializer, LineSerializer, TripPatternSerializer, CalendarSerializer


__author__ = 'Joel Haasnoot'

# TODO: Figure out DetailSerializerMixin
class LineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LineSerializer
    # serializer_detail_class = LineSerializer
    queryset = Line.objects.all()

    def get_user_agency(self):
        if self.request.user.profile:
            return self.request.user.profile.default_agency.pk
        return None

    def get_queryset(self):
        return super(LineViewSet, self).get_queryset().filter(agency=self.get_user_agency())


class AuthenticatedModelViewSet(viewsets.ModelViewSet):
    def get_user_agency(self):
        if self.request.user.profile:
            return self.request.user.profile.default_agency.pk
        return None # TODO: Throw exception

class TripPatternViewSet(AuthenticatedModelViewSet):
    serializer_class = TripPatternSerializer
    queryset = TripPattern.objects.all()

    def get_queryset(self):
        # This is our authentication
        return super(AuthenticatedModelViewSet, self).get_queryset().filter(agency=self.get_user_agency())

    @detail_route(methods=['POST'])
    def clone(self, request, pk=None):
        response = self.get_object().clone()

        serialize = TripPatternSerializer(response)
        return Response(serialize.data)

    @detail_route(methods=['POST'])
    def insert_stop(self, request, pk=None):
        pattern = self.get_object()

        # TODO: returning a single pattern stop, but we've changed more than just taht
        response = pattern.insert_stop(request.data['stop'], request.data['pre'], request.data['post'])
        serialize = TripPatternStopSerializer(response)
        return Response(serialize.data)

class CalendarViewSet(AuthenticatedModelViewSet):
    serializer_class = CalendarSerializer
    queryset = Calendar.objects.all()

    def get_queryset(self):
        # This is our authentication
        return super(AuthenticatedModelViewSet, self).get_queryset().filter(agency=self.get_user_agency())

    def create(self, request, *args, **kwargs):
        request.data['agency'] = str(self.get_user_agency());
        return super(CalendarViewSet, self).create(request, *args, **kwargs)


router = routers.SimpleRouter()
router.register(r'data/line_details', LineViewSet)
router.register(r'data/trip_patterns', TripPatternViewSet)
router.register(r'data/calendars', CalendarViewSet)