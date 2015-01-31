from rest_framework import serializers, routers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin
from data.models import Line, TripPattern, Stop, Trip, TripPatternStop

__author__ = 'Joel Haasnoot'


class TripPatternStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripPatternStop
        fields = ('id', 'order', 'stop', 'arrival_delta', 'departure_delta')


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('id', 'start_time', 'calendar')


class TripPatternSerializer(serializers.ModelSerializer):
    stops = TripPatternStopSerializer(many=True, read_only=True)
    trips = TripSerializer(many=True, read_only=True)

    class Meta:
        model = TripPattern
        fields = ('id', 'is_forward', 'stops', 'trips')


# class LineListSerializer(serializers.ModelSerializer):
#     agency = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Line
#         fields = ('id', 'planning_number', 'public_number', 'agency')


class LineSerializer(serializers.ModelSerializer):
    agency = serializers.PrimaryKeyRelatedField(read_only=True)
    patterns = TripPatternSerializer(read_only=True, many=True)

    class Meta:
        model = Line
        fields = ('id', 'planning_number', 'public_number', 'agency', 'patterns')
        depth = 3

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


class TripPatternViewSet(viewsets.ModelViewSet):
    serializer_class = TripPatternSerializer
    queryset = TripPattern.objects.all()

    def get_user_agency(self):
        if self.request.user.profile:
            return self.request.user.profile.default_agency.pk
        return None

    def get_queryset(self):
        # This is our authentication
        return super(TripPatternViewSet, self).get_queryset().filter(line__agency=self.get_user_agency())

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


router = routers.SimpleRouter()
router.register(r'data/line_details', LineViewSet)
router.register(r'data/trip_patterns', TripPatternViewSet)