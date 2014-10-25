/**
 * Created by joelthuis on 24/10/14.
 */

var drglServices = angular.module('drglServices', ['ngResource']);

drglServices.factory('Line', [''])

drglServices.factory('Line', ['$resource', function($resource) {
    return $resource('/data/line/', {'pk': '@pk'},
        {getPatterns : {method: "GET", url: '/data/line/patterns/', isArray: true}});
}]);

drglServices.factory('Stop', ['$resource', function($resource) {
    return $resource('/data/stop/', {'pk': '@pk'}, {});
}]);

drglServices.factory('TripPattern', ['$resource', function($resource) {
    return $resource('/data/trip_pattern/', {'pk': '@pk'},
        {getStops : {method: "GET", url: '/data/trip_pattern/stops/', isArray: true},
         getTrips : {method: "GET", url: '/data/trip_pattern/trips/', isArray: true}});
}]);

drglServices.factory('TripPatternStop', ['$resource', function($resource) {
    return $resource('/data/trip_pattern_stop/', {'pk': '@pk'}, {});
}]);

drglServices.factory('Trip', ['$resource', function($resource) {
    return $resource('/data/trip/', {'pk': '@pk'}, {});
}]);
