from rest_framework import serializers, routers, viewsets
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
    #serializer_detail_class = LineSerializer
    queryset = Line.objects.all()

    def get_queryset(self):
        return super(LineViewSet, self).get_queryset()


router = routers.DefaultRouter()
router.register(r'data/line_details', LineViewSet)