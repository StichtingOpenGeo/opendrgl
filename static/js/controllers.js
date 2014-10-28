/**
 * Created by joelthuis on 23/08/14.
 */

var drglApp = angular.module('drglApp', ['ngCookies', 'ngRoute', 'drglServices']);

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

drglApp.controller('LineOverviewCtrl', ['$scope', 'Line', function($scope, Line) {
    $scope.lines = Line.query();
    $scope.agency = 2
    $scope.newLine = {}
    $scope.addLine = function() {
        var line = new Line({ public_number: $scope.newLine.number, planning_number: $scope.newLine.number, agency: $scope.agency  });
        line.$save(function() {
            $scope.newLine = {};
            $scope.lines = Line.query(); // Reload
        })
    }
}]);

drglApp.controller('LineEditCtrl', ['$scope', '$routeParams', 'Line', 'Stop', function($scope, $routeParams, Line, Stop) {
    $scope.line_id = $routeParams['line']
    $scope.line = Line.get({pk: $routeParams['line']})
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

    $scope.getStops = function() {
        if (Object.keys($scope.patterns).length > 0) {
            var stops = []
            angular.forEach($scope.patterns, function(pattern, pk) {
               if (stops.length == 0) {
                   angular.forEach(pattern.stops, function(stop) {
                       stops.push(stop);
                   });
               } else {
                   // TODO Check if we need to add more stops for more patterns
                   // Complex matching algorithm here :P
               }
            });
            return stops;
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
        var startTime = ($scope.trips.length) ? $scope.trips[$scope.trips.length-1].start_time + 60 : 32400;
        var t = new Trip({ pattern: defaultPattern, start_time: startTime });
        t.$save(function(t) {
            t.stops = $scope.cloneStops(defaultPattern, startTime);
            t.first = false;
            t.start_time_written = $scope.printTime($scope.parseSeconds(startTime))
            $scope.trips.push(t);
            var tripIndex = $scope.trips.length - 1
            $scope.$watch('trips['+tripIndex+'].start_time_written', $scope.handleTripStartChangeListener(tripIndex));
        });
    }
    $scope.addStop = function() {
        var stopId = parseInt($scope.getHighestStop()) + 1;
        var s = new Stop({  agency: $scope.line.agency,
            name: $scope.newStop.name,
            planning_number: stopId,
            public_number: stopId })
        s.$save(function(stop) {
            $scope.stops[stop.pk] = stop;
            if (Object.keys($scope.patterns).length == 0) {
                var tp = new TripPattern({line: $scope.line_id, is_forward: $scope.isForward})
                tp.$save(function(pattern) {
                    pattern.stops = []
                    $scope.patterns[pattern.pk] = pattern;
                    $scope.addTrip() /* add atleast one trip*/
                });
            }
            angular.forEach($scope.patterns, function (pattern, pk) {
                var tps = new TripPatternStop({pattern: pattern.pk, stop: stop.pk,
                    order: $scope.getMaxOrder(pattern.stops) + 1  });
                tps.$save(function(patternstop) {
                    pattern.stops.push(patternstop);
                    $scope.current_stops = $scope.getStops();
                    var stopIndex = $scope.patterns[pk].stops.length - 1
                    $scope.$watch('patterns['+pk+'].stops['+stopIndex+'].departure_time', $scope.handleTripTimeChangeListener(pattern, stopIndex));
                }).then(function() {
                    angular.forEach($scope.trips, function(trip, index) {
                        trip.stops = $scope.cloneStops(trip.pattern, trip.start_time);
                    });
                })

            });
            $scope.newStop = { name: "" }
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

    $scope.cloneStops = function(pattern, start_time) {
        var stops = []
        if (!$scope.patterns[pattern] || $scope.patterns[pattern].stops.length == 0) {
            return stops;
        }

        angular.forEach($scope.patterns[pattern].stops, function(stop, stopIndex) {
            var new_stop = {arrival_delta: stop.arrival_delta,
                            departure_delta: stop.departure_delta,
                            order: stop.order,
                            pattern: stop.pattern,
                            pk: stop.pk,
                            stop: stop.stop,
                            time: $scope.printTime($scope.parseSeconds(start_time + stop.departure_delta))
                            }
            stops.push(new_stop);
        });
        return stops
    }
    $scope.removeStop = function(patternStop) {
        TripPatternStop.delete({pk: patternStop.pk}, function(deletedPattern) {
            var i = $scope.patterns[deletedPattern.pattern].stops.indexOf(patternStop);
            $scope.patterns[deletedPattern.pattern].stops.splice(i, 1);
            $scope.current_stops = $scope.getStops();
        });
    }
    $scope.removeTrip = function(trip) {
        Trip.delete({pk: trip.pk}, function(deleted) {
            var i = $scope.trips.indexOf(trip)
            $scope.trips.splice(i, 1)
        });
    }
    $scope.parseTime = function(input) {
        if (input == null) {
            return null;
        }
        var out = new Date();
        var split = input.split(':');
        out.setHours(parseInt(split[0]));
        out.setMinutes(parseInt(split[1]));
        out.setSeconds(parseInt(split[2]));
        return out;
    }
    $scope.parseTimeToSeconds = function(input) {
        if (input == null) {
            return null;
        }
        var split = input.split(':');
        return parseInt(split[0]) * 60*60 + parseInt(split[1]) * 60 + parseInt(split[2]) ;
    }
    $scope.padTime = function(input) {
        if (input < 10) {
            return "0" + input;
        }
        return input
    }
    $scope.printTime = function(time) {
        return $scope.padTime(time.getHours())+":"+$scope.padTime(time.getMinutes())+":"+$scope.padTime(time.getSeconds());
    }
    $scope.handleTripStartChangeListener = function(tripIndex) {
        return function(newVal, oldVal, scope) {
           if (oldVal !== newVal && $scope.parseTime(newVal) != null) {
               Trip.get({pk: $scope.trips[tripIndex].pk}, function(trip) {
                trip.start_time = $scope.parseDateToSeconds($scope.parseTime(newVal));
                trip.$save();
                /* Make sure to update times */
                $scope.trips[tripIndex].stops = $scope.cloneStops(trip.pattern, trip.start_time);
               });
           }
        }
    }
    $scope.handleTripTimeChangeListener = function(pattern, stopIndex) {
        return function(newVal, oldVal, scope) {
            if (oldVal !== newVal && $scope.parseTime(newVal) != null) {
                TripPatternStop.get({pk: pattern.stops[stopIndex].pk}, function (tps) {
                    newVal = Math.max($scope.parseTimeToSeconds(newVal) - $scope.trips[pattern.trip_index].start_time, 0)
                    if (tps.departure_delta != newVal) {
                        tps.departure_delta = newVal;
                        tps.$save()
                        /* Make sure to update times */
                        pattern.stops[stopIndex].departure_delta = newVal;
                        angular.forEach($scope.trips, function(trip, index) {
                            trip.stops = $scope.cloneStops(trip.pattern, trip.start_time);
                        });
                    }
                });
            }
        }
    };

    $scope.parseSeconds = function (baseSeconds) {
        var time = new Date();
        var hours   = Math.floor(baseSeconds / 3600);
        var minutes = Math.floor((baseSeconds - (hours * 3600)) / 60);
        time.setHours(hours, minutes, baseSeconds - (hours * 3600) - (minutes * 60))
        return time
    };
    $scope.parseDateToSeconds = function(date) {
        return date.getSeconds() + date.getMinutes() * 60 + date.getHours() * 60 * 60;
    }
    $scope.getPatterns = function() {
        Line.getPatterns({ line: $scope.line_id, is_forward: $scope.isForward }, function(patterns) {
            angular.forEach(patterns, function(pattern, patternId) {
                TripPattern.getStops({pattern: pattern.pk}, function(retrieved_pattern) {
                    $scope.patterns[pattern.pk] = pattern
                    $scope.patterns[pattern.pk].stops = (retrieved_pattern.length == 0) ? [] : retrieved_pattern;
                    $scope.current_stops = $scope.getStops();
                    angular.forEach(retrieved_pattern, function(stop, stopIndex) {
                        $scope.$watch('patterns['+pattern.pk+'].stops['+stopIndex+'].departure_time', $scope.handleTripTimeChangeListener(pattern, stopIndex));
                    });
                });
                TripPattern.getTrips({pattern: pattern.pk}, function(trips) {
                    var first = true;
                    angular.forEach(trips, function(trip) {
                        trip.first = first;
                        trip.start_time_written = $scope.printTime($scope.parseSeconds(trip.start_time))
                        trip.stops = $scope.cloneStops(pattern.pk, trip.start_time);
                        $scope.trips.push(trip);
                        var tripIndex = $scope.trips.length - 1;
                        $scope.$watch('trips['+tripIndex+'].start_time_written', $scope.handleTripStartChangeListener(tripIndex));
                        if (first) {
                            pattern.trip_index = tripIndex;
                            if ($scope.patterns[pattern.pk] && $scope.patterns[pattern.pk].stops > 0) {
                                angular.forEach($scope.patterns[pattern.pk].stops, function (stop) {
                                    stop.departure_time = $scope.printTime($scope.parseSeconds(trip.start_time + stop.departure_delta))
                                });
                            }
                            first = false;
                        }
                    });
                    angular.forEach($scope.trips, function(trip, index) {
                        trip.stops = $scope.cloneStops(trip.pattern, trip.start_time);
                    });
                });
            });
        });
    }
    $scope.getPatterns();
//        $scope.recalculateDiffs = function() {
//        $scope.diffs = [];
//        var stops = $scope.getStops();
//        var cur, next;
//        for (var i = 0; i < stops.length-1; i++) {
//            cur = $scope.parseTime(stops[i].time);
//            next = $scope.parseTime(stops[i+1].time);
//            $scope.diffs.push(next-cur);
//        }
//    }
//    $scope.recalculateTrips = function() {
//        for (var i = 1; i < $scope.trips.length; i++) {
//            $scope.recalculateTrip($scope.trips[i]);
//        }
//    }
//    $scope.recalculateTrip = function(trip) {
//        var prev = $scope.parseTime(trip.stops[0].time);
//        var newTime;
//        for (var i = 1; i < trip.stops.length; i++) {
//            newTime = new Date(prev);
//            newTime.setMilliseconds(newTime.getMilliseconds() + $scope.diffs[i-1])
//            trip.stops[i].time = $scope.printTime(newTime);
//            prev = $scope.parseTime(trip.stops[i].time);
//        }
//    }
}]);


drglApp.config(['$routeProvider', '$resourceProvider', function($routeProvider, $resourceProvider) {

    $resourceProvider.defaults.stripTrailingSlashes = false;

    $routeProvider
        .when('/line/:line', {
            templateUrl: 'js/templates/line_edit.html',
            controller: 'LineEditCtrl'
        })
        .when('/', {
            templateUrl: 'js/templates/line_overview.html',
            controller: 'LineOverviewCtrl'
        });
}]);