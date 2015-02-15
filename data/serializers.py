from rest_framework import serializers
from data.models import TripPatternStop, Trip, TripPattern, Line, CalendarException, Calendar, Agency

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


class CalendarExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarException
        fields = ('is_cancel', 'date')


class CalendarSerializer(serializers.ModelSerializer):
    agency = serializers.PrimaryKeyRelatedField(queryset=Agency.objects.all())
    exceptions = CalendarExceptionSerializer(many=True, required=False)

    class Meta:
        model = Calendar
        fields = ('id', 'label', 'agency', 'from_date', 'till_date', 'on_monday', 'on_tuesday', 'on_wednesday',
                  'on_thursday', 'on_friday', 'on_saturday', 'on_sunday', 'exceptions')
        depth = 1