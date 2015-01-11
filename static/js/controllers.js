/**
 * Created by Joel Haasnoot on 23/08/14.
 */
var template_dir = '/static/js/templates/'
var openDrglApp = angular.module('openDrglApp', ['ngCookies', 'ngRoute', 'openDrglUtils', 'openDrglServices', 'ui.bootstrap', 'openlayers-directive']);

openDrglApp.run(function($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});

openDrglApp.directive('scheduleTable', function() {
    return {
        restrict: 'E',
        templateUrl: template_dir+'schedule_table.html',
        scope: {
            lineDirectionForward: "="
        }
    };
});

openDrglApp.controller('LineOverviewCtrl', ['$scope', 'LineService', function($scope, LineService) {
    $scope.lines = [];
    $scope.agency = 2; 
    $scope.newLine = {};
    this.loadLines = function() {
        LineService.getLines().then(function(lines) {
            $scope.lines = lines;
        });
    };
    $scope.addLine = function() {
        var line = LineService.createLine({ public_number: $scope.newLine.number, planning_number: $scope.newLine.number, agency: $scope.agency });
        LineService.saveLine(line).then(function(line) {
            $scope.newLine = {};
            $scope.lines.push(line);
        })
    }
    this.loadLines();
}]);

openDrglApp.controller('LineEditCtrl', ['$scope', '$routeParams', 'LineService', 'StopService', function($scope, $routeParams, LineService, StopService) {
    $scope.line_id = $routeParams['line']
    $scope.line = {};
    LineService.getLine($routeParams['line']).then(function(line) {
        $scope.line = line;
    })
}]);

openDrglApp.controller('ScheduleCtrl', ['$scope', '$http', '$log', 'LineService', 'TripPatternStopService',
        'TripService', 'StopService', 'StringUtils', 'MathUtils', 'TimeUtils', 'ArrayUtils',
    function ($scope, $http, $log, LineService, TripPatternStopService, TripService, StopService, StringUtils, MathUtils, TimeUtils, ArrayUtils) {
    $scope.colors = ["#FF8A80", "#FF8A80", "#B388FF", "#8C9EFF", "#82B1FF"];
    $scope.lastTripId = 2;
    $scope.newStop = { name: ""}
    $scope.current_stops = [];
    $scope.diffs = [];
    $scope.patterns = {};
    $scope.trips = [];

    $scope.getStops = function() {
        if (Object.keys($scope.patterns).length > 0) {
            var stops = []
            angular.forEach($scope.patterns, function(pattern, pk) {
               if (stops.length == 0) {
                   /* First run is naive */
                   stops = pattern.stops;
               } else {
                   // TODO Check if we need to add more stops for more patterns
                   // Complex matching algorithm here :P
                   stops = ArrayUtils.sortByKey(ArrayUtils.uniqueDicts(stops.concat(pattern.stops), 'stop'), 'order');
               }
            });
            return stops;
        } else {
            return [];
        }
    }
    $scope.getTime = function(trip, index) {
        return $scope.patterns[trip.pattern].stops[index].time;
    }
    $scope.getPatternCell = function(patternIndex, stopIndex) {
        return $scope.patterns[patternIndex].current_stops[stopIndex].departure_time;
    }
    $scope.addTrip = function() {
        $scope.lastTripId += 1;
        var defaultPattern = $scope.patterns[Object.keys($scope.patterns)[0]].id;
        var startTime = ($scope.trips.length) ? $scope.trips[$scope.trips.length-1].start_time + 60 : 32400;
        var t = TripService.createTrip({ pattern: defaultPattern, start_time: startTime });
        TripService.saveTrip(t).then($scope.initTrip);
    }
    $scope.initTrip = function(newTrip) {
        newTrip.stops = $scope.cloneStops(newTrip.pattern, newTrip.start_time);
        // TODO: determine first properly
        newTrip.first = false;
        newTrip.start_time_written = TimeUtils.printSeconds(newTrip.start_time)
        $scope.trips.push(newTrip);
        // TODO: this is the second place this gets done
        var tripIndex = $scope.trips.length - 1
        $scope.$watch('trips['+tripIndex+'].start_time_written', $scope.handleTripStartChangeListener(tripIndex));
    }

    $scope.selectNewStop = function(item, model, label) {
        $scope.newStop.name = model.name;
        $scope.newStop.city = model.city;
        $scope.newStop.public_number = model.public_code;
        $scope.newStop.planning_number = StringUtils.splitChbId(model.public_code);
        $scope.newStop.lat = model.lat;
        $scope.newStop.lon = model.lon;
        $scope.addStop()
    }
    $scope.addStop = function() {
        var s = StopService.newStop({
            agency: 2,
            name: $scope.newStop.name
        });
        /* Check if this is a new custom stop or one from CHB */
        if ($scope.newStop.public_number) {
            s.public_number = $scope.newStop.public_number;
            s.planning_number = $scope.newStop.planning_number;
            s.lat = $scope.newStop.lat;
            s.lon = $scope.newStop.lon;
        }
        StopService.saveStop(s)
            .then($scope.initStop)
            .then(function() {
                $scope.newStop = {name: ""};
            })
            .catch($log.error);
    };
    $scope.initPatternStop = function(patternstop) {
        var pattern = $scope.patterns[patternstop.pattern];
        patternstop.departure_time = TimeUtils.printSeconds($scope.trips[pattern.trip_index].start_time + patternstop.departure_delta)
        pattern.stops.push(patternstop);
        $scope.current_stops = $scope.getStops();
        $scope.recalculateCurrentPatternStops(); /* Recalculate current stops for each pattern */
        var stopIndex = pattern.stops.length - 1
        // TODO: this is the second place this gets done
        $scope.$watch('patterns[' + pattern.id + '].stops[' + stopIndex + '].departure_time', $scope.handleTripTimeChangeListener(pattern, stopIndex));
    }
    $scope.initStop = function(stop) {
        stop.id = stop.pk;
        $scope.stops[stop.id] = stop; /* Add to local other cache? TODO: FIX */
        StopService.addStopToCache(stop);
        $scope.calculateTripPattern(stop);
    }
    $scope.calculateTripPattern = function(stop) {
        angular.forEach($scope.patterns, function (pattern, pk) {
            var lastStop = pattern.stops[pattern.stops.length - 1];
            var departure_delta = (lastStop) ? lastStop.departure_delta : 0;
            var tps = TripPatternStopService.newTripPatternStop({
                pattern: pattern.id,
                stop: stop.id,
                order: MathUtils.getMaxOrder(pattern.stops) + 1,
                arrival_delta: departure_delta,
                departure_delta: departure_delta
            });
            TripPatternStopService.saveTripPatternStop(tps)
                .then($scope.initPatternStop)
                .then(function () {
                    angular.forEach($scope.trips, function (trip, index) {
                        trip.stops = $scope.cloneStops(trip.pattern, trip.start_time);
                    });
                })

        });
    };
    $scope.getStopSearch = function(val) {
        return $http.get('/data/chb?name='+val, {}).then(function(response){
            return response.data.map(function(stop) {
                stop['label'] = stop.city+", "+stop.name
                return stop
            });
        });
    };
    $scope.getStopDetails = function(stop_id) {
        return $scope.stops[stop_id];
    }

    $scope.cloneStops = function(pattern, start_time) {
        if (!$scope.patterns[pattern] || $scope.patterns[pattern].stops.length == 0) {
            return [];
        }

        var stops = [];
        var pattern_stops = $scope.patterns[pattern].stops;
        var pattern_index = 0;
        angular.forEach($scope.current_stops, function(tps, stopIndex) {
            var new_stop;
            if (pattern_stops[pattern_index] == null || pattern_stops[pattern_index].stop != tps.stop) {
                /* If the id's aren't equal, insert a blank stop */
                new_stop = {}
            } else {
                var stop = pattern_stops[pattern_index];
                new_stop = {
                    arrival_delta: stop.arrival_delta,
                    departure_delta: stop.departure_delta,
                    order: stop.order,
                    pattern: stop.pattern,
                    pk: stop.id,
                    stop: stop.stop,
                    time: TimeUtils.printSeconds(start_time + stop.departure_delta)
                };
                pattern_index = pattern_index + 1;
            }
            stops.push(new_stop);
        });
        return stops
    }
    $scope.removeStopFromPattern = function(pattern, stopIndex) {
        var tps = $scope.patterns[pattern].current_stops[stopIndex];
        TripPatternStopService.deleteTripPatternStop(tps.id)
            .then(function(deletedStop) {
                var pattern = $scope.patterns[deletedStop.pattern];
                var i = pattern.stops.indexOf(tps);
                pattern.stops.splice(i, 1);
                $scope.current_stops = $scope.getStops();
                // TODO: only do this for trips in this pattern
                angular.forEach($scope.trips, function(trip, index) {
                    trip.stops = $scope.cloneStops(trip.pattern, trip.start_time);
                });
                pattern.current_stops = $scope.getCurrentStopPattern(pattern.id);
            });
    }
    $scope.removeTrip = function(trip) {
        if ($scope.trips.length == 1) {
            return; // Can't delete last trip
        }

        TripService.deleteTrip(trip.id)
            .then(function(deleted) {
                var i = $scope.trips.indexOf(trip)
                $scope.trips.splice(i, 1)
                if (trip.first) {
                    /* Find the new first pattern */
                    $scope.trips[0].first = true;
                    // TODO: This won't work for multiple patterns :(
                    /* Recalculate our departure_times */
                    angular.forEach($scope.patterns[$scope.trips[0].pattern].stops, function (stop) {
                        stop.departure_time = TimeUtils.printSeconds($scope.trips[0].start_time + stop.departure_delta);
                    });
                }
            });
    }
    $scope.handleTripStartChangeListener = function(tripIndex) {
        return function(newVal, oldVal, scope) {
           if (oldVal !== newVal && TimeUtils.parseTime(newVal) != null) {
               /* TODO: Get the current trip to...? Ensure we're still on the same page? */
               TripService.getTrip($scope.trips[tripIndex].id)
                   .then(function(trip) {
                       trip.start_time = TimeUtils.parseDateToSeconds(TimeUtils.parseTime(newVal));
                       TripService.saveTrip(trip).then(function(savedTrip) {
                           /* Make sure to update times */
                           var localTrip = $scope.trips[tripIndex];
                           localTrip.start_time = savedTrip.start_time;
                           localTrip.stops = $scope.cloneStops(savedTrip.pattern, savedTrip.start_time);
                       });
                   }).catch($log.error);
           }
        }
    }
    $scope.handleTripTimeChangeListener = function(pattern, stopIndex) {
        return function(newVal, oldVal, scope) {
            if (oldVal !== newVal && TimeUtils.parseTime(newVal) != null) {
                TripPatternStopService.getTripPatternStop(pattern.stops[stopIndex].id).then(function (tps) {
                    newVal = Math.max(TimeUtils.parseTimeToSeconds(newVal) - $scope.trips[pattern.trip_index].start_time, 0)
                    if (tps.departure_delta != newVal) {
                        tps.departure_delta = newVal;
                        TripPatternStopService.saveTripPatternStop(tps).then(function(tps) {
                            /* Make sure to update times */
                            pattern.stops[stopIndex].departure_delta = newVal;
                            angular.forEach($scope.trips, function(trip, index) {
                                trip.stops = $scope.cloneStops(trip.pattern, trip.start_time);
                            });
                        });
                    }
                });
            }
        }
    };
    $scope.getCurrentStopPattern = function(pattern) {
        var stops = [];
        var pattern_stops = $scope.patterns[pattern].stops;
        var pattern_index = 0;
        angular.forEach($scope.current_stops, function(tps, stopIndex) {
            var new_stop;
            if (pattern_stops[pattern_index] == null || pattern_stops[pattern_index].stop != tps.stop) {
                /* If the id's aren't equal, insert a blank stop */
                new_stop = {}
            } else {
                new_stop = pattern_stops[pattern_index];
                pattern_index = pattern_index + 1;
            }
            stops.push(new_stop);
        });
        return stops;
    };
    $scope.getPatterns = function() {
        LineService.getLineDetails($scope.$parent.$parent.line_id).then(function(details) {
            angular.forEach(details.patterns, function (pattern, patternIndex) {
                if (pattern.is_forward != $scope.$parent.lineDirectionForward) {
                    return;
                }

                pattern.stops = ArrayUtils.sortByKey(pattern.stops, 'order');
                pattern.color = $scope.colors[patternIndex];
                $scope.patterns[pattern.id] = pattern;

                angular.forEach(pattern.stops, function (stop, stopIndex) {
                    $scope.$watch('patterns[' + pattern.id + '].stops[' + stopIndex + '].departure_time', $scope.handleTripTimeChangeListener(pattern, stopIndex));
                });

                var first = true;
                pattern.trips.sort(function(a, b) { return a.start_time - b.start_time; });
                angular.forEach(pattern.trips, function (trip) {
                    trip.pattern = pattern.id;
                    trip.color = pattern.color;
                    trip.first = first;
                    trip.start_time_written = TimeUtils.printSeconds(trip.start_time);
                    $scope.trips.push(trip);
                    var tripIndex = $scope.trips.length - 1;
                    $scope.$watch('trips[' + tripIndex + '].start_time_written', $scope.handleTripStartChangeListener(tripIndex));
                    if (first) {
                        pattern.trip_index = tripIndex;
                        if ($scope.patterns[pattern.id] && $scope.patterns[pattern.id].stops.length > 0) {
                            angular.forEach($scope.patterns[pattern.id].stops, function (stop) {
                                stop.departure_time = TimeUtils.printSeconds(trip.start_time + stop.departure_delta)
                            });
                        }
                        first = false;
                    }
                });
            });
            $scope.trips.sort(function(a, b) { return a.start_time - b.start_time; });
            $scope.current_stops = $scope.getStops();
            angular.forEach($scope.trips, function (trip, index) {
                trip.stops = $scope.cloneStops(trip.pattern, trip.start_time);
            });
            $scope.recalculateCurrentPatternStops();
        }).catch($log.error);
    };
    $scope.recalculateCurrentPatternStops = function() {
        angular.forEach($scope.patterns, function(pattern, index) {
            $scope.patterns[pattern.id].current_stops = $scope.getCurrentStopPattern(pattern.id);
        });
    }
    $scope.init = function() {
        StopService.getAllStops()
            .then(function(stops) {
                $scope.stops = stops;
            }).
            then($scope.getPatterns);
    }
    $scope.init();
}]);

openDrglApp.controller('MapController', ['$scope', function($scope) {
    $scope.stops = [];
    angular.extend($scope, {
        layers: {
            main: {
                "source": {
                    "type": "Stamen",
                    "layer": "toner"
                },
                "visible": true,
                "opacity": 1
            }
        },
        center: {
            lat: 52.089398,
            lon: 5.109861,
            zoom: 10
        }
    });
    $scope.getMarkerStops = function() {
        $scope.stops = [];
        angular.forEach($scope.$parent.current_stops, function(pattern_stop, index) {
            var real_stop = $scope.$parent.getStopDetails(pattern_stop.stop);
            $scope.stops.push(real_stop);
        });
    };
    $scope.getMarkerStops();
    $scope.$watch('$parent.current_stops', $scope.getMarkerStops);
}])

openDrglApp.config(['$routeProvider', '$resourceProvider', function($routeProvider, $resourceProvider) {

    $resourceProvider.defaults.stripTrailingSlashes = false;

    $routeProvider
        .when('/line/:line', {
            templateUrl: template_dir+'line_edit.html',
            controller: 'LineEditCtrl'
        })
        .when('/', {
            templateUrl: template_dir+'line_overview.html',
            controller: 'LineOverviewCtrl'
        });
}]);