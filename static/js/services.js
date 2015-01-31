/**
 * Created by Joel Haasnoot on 26/12/14.
 */

var openDrglServices = angular.module('openDrglServices', ['openDrglResources']);

openDrglServices.service('LineService', ['$http', 'LineDetailsResource', 'LineResource', function($http, LineDetailsResource, LineResource) {

    this.getLines = function() {
        return LineResource.query().$promise;
    };

    this.getLine = function(line_id) {
        return LineResource.get({'pk' : line_id }).$promise;
    };

    this.getLineDetails = function(line_id) {
        return LineDetailsResource.get({id: line_id}).$promise;
    }

    this.createLine = function(args) {
        return new LineResource(args);
    };

    this.saveLine = function(line) {
        return line.$save();
    }

    this.deleteLine = function(id) {
        return LineResource.delete({'pk' : id}).$promise;
    }


}]);

openDrglServices.service('StopService', ['$q', 'StopResource', function($q, StopResource) {

    var stopCache;

    this.getAllStops = function() {
        if (stopCache) {
            return $q.when(stopCache);
        }
        /* Get all the stops but alias them by id */
        return StopResource.query().$promise.then(function(stops) {
            var result_dict = {};
            angular.forEach(stops, function(stop) {
                result_dict[stop.pk] = stop;
            });
            stopCache = result_dict;
            return result_dict;
        });
    }

    this.addStopToCache = function(stop) {
        if (!stopCache) {
            stopCache = {};
        }
        stopCache[stop.pk] = stop;
    }

    this.newStop = function(args) {
        return new StopResource(args);
    }

    this.saveStop = function(stop) {
        return stop.$save();
    }

}]);

openDrglServices.service('TripPatternService', ['PatternDetailsResource', function(PatternDetailsResource) {

    this.cloneTripPattern = function(pattern) {
        return PatternDetailsResource.clone({pk: pattern}).$promise;
    }

    this.insertStopIntoTripPattern = function(pattern, stop, pre, post)  {
        return PatternDetailsResource.insert_stop({pk: pattern, stop: stop, pre: pre, post: post}).$promise;
    }

}]);

openDrglServices.service('TripService', ['TripResource', function(TripResource) {

    this.getTrip = function(id) {
        return TripResource.get({pk: id}).$promise;
    }

    this.createTrip = function(args) {
        return new TripResource(args);
    }

    this.saveTrip = function(trip) {
        return trip.$save();
    }

    this.deleteTrip = function(id) {
        return TripResource.delete({pk: id}).$promise;
    }

}]);

openDrglServices.service('TripPatternStopService', ['TripPatternStopResource', function(TripPatternStopResource) {


    this.newTripPatternStop = function(args) {
        return new TripPatternStopResource(args);
    }

    this.saveTripPatternStop = function(tps) {
        return tps.$save();
    }

    this.deleteTripPatternStop = function(tps_id) {
        return TripPatternStopResource.delete({pk: tps_id}).$promise;
    }

    this.getTripPatternStop = function(tps_id) {
        return TripPatternStopResource.get({pk: tps_id}).$promise;
    }

}]);


openDrglServices.service('CalendarService', ['CalendarResource', function(CalendarResource) {


    this.newCalendar = function(args) {
        return new CalendarResource(args);
    }

    this.saveCalendar = function(cal) {
        return cal.$save();
    }

    this.deleteCalendar = function(id) {
        return CalendarResource.delete({pk: id}).$promise;
    }

    this.getCalendar = function(id) {
        return CalendarResource.get({pk: id}).$promise;
    }

    this.getCalendars = function(id) {
        return CalendarResource.query().$promise;
    }

}]);