/**
 * Created by joelthuis on 23/08/14.
 */
var drglApp = angular.module('drglApp', []);

drglApp.controller('ScheduleCtrl', function ($scope) {
    $scope.lastStopId = 3;
    $scope.lastTripId = 2;
    $scope.newItem = { name: ""}
    $scope.diffs = [];
    $scope.trips = [
        {
            id: 1,
            stops: [
                { id: 1, name: "Home", time: "09:00"},
                { id: 2, name: "Work", time: "09:10"},
                { id: 3, name: "Work", time: "09:15"}
            ]
        },
        {
            id: 2,
            stops: [
                { id: 1, name: "Home", time: "09:10"},
                { id: 2, name: "Work", time: "09:15"},
                { id: 3, name: "Work", time: "09:20"}
            ]
        }
    ];

    $scope.getStops = function() {
        return $scope.trips[0].stops
    }
    $scope.getTime = function(trip, index) {
        return trip.stops[index].time;
    }
    $scope.addTrip = function() {
        $scope.lastTripId += 1;
        var trip = { id: $scope.lastTripId, stops: $scope.cloneStops() }
        $scope.trips.push(trip)
        $scope.$watch('trips['+($scope.trips.length - 1)+'].stops[0].time', $scope.handleTripStartChange);

    }
    $scope.addStop = function() {
        var lastStop;
        $scope.lastStopId += 1;
        angular.forEach($scope.trips, function (trip, id) {
            lastStop = trip.stops[trip.stops.length - 1]
            trip.stops.push({ id: $scope.lastStopId, name: $scope.newStop.name, time: lastStop.time });
        });
        var lastId = $scope.trips[0].stops.length - 1;
        $scope.$watch('trips[0].stops['+lastId+'].time', $scope.handleTripTimeChange);
        $scope.newStop = { name: "" }
    }
    $scope.cloneStops = function() {
        var output = []
        angular.forEach($scope.getStops(), function (stop, id) {
            output.push({ id: stop.id, name: stop.name, time: stop.time })
        });
        return output;
    }
    $scope.parseTime = function(input) {
        var out = new Date();
        var split = input.split(':');
        out.setHours(parseInt(split[0]));
        out.setMinutes(parseInt(split[1]));
        return out;
    }
    $scope.padTime = function(input) {
//        if (input) {
//            return "00" + input.slice('-2');
//        }
        return input
    }
    $scope.printTime = function(time) {
        return $scope.padTime(time.getHours())+":"+$scope.padTime(time.getMinutes());
        //return time.getHours()+":"+time.getMinutes();
    }
    $scope.handleTripStartChange = function(newVal, oldVal) {
        if (oldVal !== newVal) {
            $scope.recalculateDiffs();
            $scope.recalculateTrips();
        }
    }
    $scope.handleTripTimeChange = function(newVal, oldVal) {
        if (oldVal !== newVal) {
            $scope.recalculateDiffs();
            $scope.recalculateTrips();
        }
    }
    $scope.recalculateDiffs = function() {
        $scope.diffs = [];
        var stops = $scope.trips[0].stops;
        var cur, next;
        for (var i = 0; i < stops.length-1; i++) {
            cur = $scope.parseTime(stops[i].time);
            next = $scope.parseTime(stops[i+1].time);
            $scope.diffs.push(next-cur);
        }
    }
    $scope.recalculateTrips = function() {
        for (var i = 1; i < $scope.trips.length; i++) {
            $scope.recalculateTrip($scope.trips[i]);
        }
    }
    $scope.recalculateTrip = function(trip) {
        var prev = $scope.parseTime(trip.stops[0].time);
        var newTime;
        for (var i = 1; i < trip.stops.length; i++) {
            newTime = new Date(prev);
            newTime.setMilliseconds(newTime.getMilliseconds() + $scope.diffs[i-1])
            trip.stops[i].time = $scope.printTime(newTime);
            prev = $scope.parseTime(trip.stops[i].time);
        }
    }
    $scope.createWatches = function () {
        angular.forEach($scope.trips, function (trip, id) {
            $scope.$watch('trips['+id+'].stops[0].time', $scope.handleTripStartChange);
        });
        angular.forEach($scope.trips[0].stops, function(stop, id) {
            $scope.$watch('trips[0].stops['+id+'].time', $scope.handleTripTimeChange);
        });
    };
    $scope.createWatches();
});