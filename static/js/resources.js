/**
 * Created by Joel Haasnoot on 24/10/14.
 */

var openDrglResources = angular.module('openDrglResources', ['ngResource']);

openDrglResources.factory('LineResource', ['$resource', function($resource) {
    return $resource('/data/line/', {'pk': '@pk'},
        {getPatterns : {method: "GET", url: '/data/line/patterns/', isArray: true}});
}]);

openDrglResources.factory('StopResource', ['$resource', function($resource) {
    return $resource('/data/stop/', {'pk': '@pk'}, {});
}]);

openDrglResources.factory('TripPatternResource', ['$resource', function($resource) {
    return $resource('/data/trip_pattern/', {'pk': '@pk'},
        {getStops : {method: "GET", url: '/data/trip_pattern/stops/', isArray: true},
         getTrips : {method: "GET", url: '/data/trip_pattern/trips/', isArray: true}});
}]);

openDrglResources.factory('TripPatternStopResource', ['$resource', function($resource) {
    return $resource('/data/trip_pattern_stop/', {'pk': '@pk'}, {});
}]);

openDrglResources.factory('TripResource', ['$resource', function($resource) {
    return $resource('/data/trip/', {'pk': '@pk'}, {});
}]);
