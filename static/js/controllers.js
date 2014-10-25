/**
 * Created by joelthuis on 23/08/14.
 */

var drglApp = angular.module('drglApp', ['ngCookies', 'drglServices']);

drglApp.run(function($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});

drglApp.directive('scheduleTable', function() {
    return {
        restrict: 'E',
        templateUrl: 'js/templates/scheduleTable.html'
    };
});

drglApp.controller('LineCtrl', ['$scope', 'Stop', function($scope, Stop) {
    $scope.agency_id = 2
    $scope.line_id = 1
    $scope.stops = {}
    $scope.getStops = function() {
        Stop.query(function(stops) {
            angular.forEach(stops, function(stop) {
                $scope.stops[stop.pk] = stop;
            });
        });
    }
    $scope.getStops();
}]);

drglApp.controller('ScheduleCtrl', ['$scope', 'Line', 'TripPattern', 'TripPatternStop', 'Trip', 'Stop',
    function ($scope, Line, TripPattern, TripPatternStop, Trip, Stop) {
    $scope.lastTripId = 2;
    $scope.newItem = { name: ""}
    $scope.current_stops = [];
    $scope.diffs = [];
    $scope.patterns = {};
    $scope.trips = [];

//    $scope.patterns = {
//        1: {
//            pk: 1,
//            stops: [
//                { id: 1, order: 1, name: "Home", time: "09:00"},
//                { id: 2, order: 2, name: "Work", time: "09:10"},
//                { id: 2, order: 3, name: "Work", time: "09:15"}
//            ]
//        }
//    }
//    $scope.trips = [
//        {
//            pk: 1,
//            pattern: 1,
//            first: true,
//            start_time: "09:00",
//            stops: [
//                { id: 1, order: 1, name: "Home", time: "09:00"},
//                { id: 2, order: 2, name: "Work", time: "09:10"},
//                { id: 2, order: 3, name: "Work", time: "09:15"}
//            ]
//        },
//        {
//            pk: 2,
//            pattern: 1,
//            first: false,
//            start_time: "09:30",
//            stops: [
//                { id: 1, order: 1, name: "Home", time: "09:30"},
//                { id: 2, order: 2, name: "Work", time: "09:40"},
//                { id: 2, order: 3, name: "Work", time: "09:45"}
//            ]
//        }
//    ];
    $scope.getStops = function() {
        if ($scope.patterns[1] != null) {
            return $scope.patterns[1].stops;
        } else {
            return [];
        }
    }
    $scope.getTime = function(trip, index) {
        pattern = $scope.patterns[trip.pattern]
        return pattern.stops[index].time;
    }
    $scope.addTrip = function() {
        $scope.lastTripId += 1;
        var defaultPattern = $scope.patterns[Object.keys($scope.patterns)[0]].pk;
        var startTime = $scope.parseTime($scope.trips[$scope.trips.length-1].start_time);
        startTime.setMinutes(startTime.getMinutes()+1);
        var t = new Trip({ pattern: trip.pattern, start_time: trip.start_time });
        t.$save(function(t) {
            var trip = { id: $scope.lastTripId, pattern: defaultPattern, start_time: $scope.printTime(startTime), stops: $scope.cloneStops() }
            $scope.trips.push(trip);
            var tripIndex = $scope.trips.length - 1
            $scope.$watch('trips['+tripIndex+'].start_time', $scope.handleTripStartChangeListener(tripIndex));
        });
    }
    $scope.getHighestStop = function() {
        var highest = -1;
        for (key in $scope.stops) {
            if (parseInt($scope.stops[key].public_number) > highest) {
                highest = parseInt($scope.stops[key].public_number)
            }
        }
        return highest;
    }
    $scope.getMaxOrder = function(arr) {
        var highest = -1;
        for (key in arr) {
            var numOrder = parseInt(arr[key].order)
            if (numOrder > highest) {
                highest = numOrder;
            }
        }
        return highest
    }
    $scope.addStop = function() {
        var stopId = parseInt($scope.getHighestStop()) + 1;
        var s = new Stop({  agency: $scope.agency_id,
                            name: $scope.newStop.name,
                            planning_number: stopId,
                            public_number: stopId })
        s.$save(function(stop) {
            $scope.stops[stop.pk] = stop;
            angular.forEach($scope.patterns, function (pattern, pk) {
                var tps = new TripPatternStop({pattern: pattern.pk, stop: stop.pk,
                                                order: $scope.getMaxOrder(pattern.stops) + 1  });
                tps.$save(function(patternstop) {
                    pattern.stops.push(patternstop);
                });
                var stopIndex = $scope.patterns[pk].stops.length - 1
                $scope.$watch('patterns[pk].stops['+stopIndex+'].departure_delta', $scope.handleTripTimeChangeListener(pattern, stopIndex));
//                lastStop = trip.stops[trip.stops.length - 1]
//                trip.stops.push({ id: s.pk, name: $scope.newStop.name, time: lastStop.time });
            });
//            var lastId = $scope.trips[0].stops.length - 1;

            $scope.newStop = { name: "" }
        });
    }
    $scope.cloneStops = function() {
        var output = []
        angular.forEach($scope.getStops(), function (stop, id) {
            output.push({ id: stop.id, name: stop.name, time: stop.time })
        });
        return output;
    }
    $scope.removeStop = function(patternStop) {
        TripPatternStop.delete({pk: patternStop.pk}, function(deletedPattern) {
            var i = $scope.patterns[deletedPattern.pattern].stops.indexOf(patternStop);
            $scope.patterns[deletedPattern.pattern].stops.splice(i, 1);
            $scope.current_stops = $scope.getStops();
        });
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
        return $scope.padTime(time.getHours())+":"+$scope.padTime(time.getMinutes())+":"+$scope.padTime(time.getSeconds());
    }
    $scope.handleTripStartChangeListener = function(tripIndex) {
        return function(newVal, oldVal, scope) {
           if (oldVal !== newVal && $scope.parseTime(newVal) != null) {
               Trip.get({pk: $scope.trips[tripIndex].pk}, function(trip) {
                trip.start_time = newVal;
                trip.$save();
               });
           }
        }
    }
    $scope.handleTripTimeChangeListener = function(pattern, stopIndex) {
        return function(newVal, oldVal) {
            if (oldVal !== newVal) {
                console.log("Changed pattern time " +pattern+" and stop " + stopIndex);
            }
        }
    };
    $scope.recalculateDiffs = function() {
        $scope.diffs = [];
        var stops = $scope.getStops();
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
    $scope.getPatterns = function() {
        Line.getPatterns({ line: $scope.line_id, is_forward: $scope.isForward }, function(patterns) {
            angular.forEach(patterns, function(pattern, patternId) {
                TripPattern.getStops({pattern: pattern.pk}, function(retrieved_pattern) {
                    $scope.patterns[pattern.pk] = { pk: pattern.pk, stops: retrieved_pattern};
                    $scope.current_stops = $scope.getStops();
                    angular.forEach(retrieved_pattern, function(stop, stopIndex) {
                        $scope.$watch('pattern['+patternId+'].stops['+stopIndex+'].departure_delta', $scope.handleTripTimeChangeListener(patternId, stopIndex));
                    });
                });
                TripPattern.getTrips({pattern: pattern.pk}, function(trips) {
                    var first = true;
                    angular.forEach(trips, function(trip) {
                        // stops: $scope.patterns[pattern].stops
                        $scope.trips.push({ pk: trip.pk, first: first, pattern: pattern.pk, start_time: trip.start_time });
                        var tripIndex = $scope.trips.length - 1;
                        $scope.$watch('trips['+tripIndex+'].start_time', $scope.handleTripStartChangeListener(tripIndex));
                        if (first) {
                            first = false;
                        }
                    });
                });
            });
        });
    }
    $scope.getPatterns();
}]);