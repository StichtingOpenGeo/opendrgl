/**
 * Created by Joel Haasnoot on 24/10/14.
 */

var openDrglResources = angular.module('openDrglResources', ['ngResource']);

openDrglResources.factory('LineResource', ['$resource', function($resource) {
    return $resource('/data/line/', {'pk': '@pk'}, {});
}]);

openDrglResources.factory('LineDetailsResource', ['$resource', function($resource) {
    return $resource('/data/line_details/:id', {'id': '@id'}, {});
}]);

openDrglResources.factory('StopResource', ['$resource', function($resource) {
    return $resource('/data/stop/', {'pk': '@pk'}, {});
}]);

openDrglResources.factory('TripPatternResource', ['$resource', function($resource) {
    return $resource('/data/trip_pattern/', {'pk': '@pk'}, {});
}]);

openDrglResources.factory('PatternDetailsResource', ['$resource', function($resource) {
    return $resource('/data/trip_patterns/:id', {'id': '@pk'},
                {'clone' : {method: 'POST', url: '/data/trip_patterns/:id/clone/'},
                 'insert_stop' : {method: 'POST', url: '/data/trip_patterns/:id/insert_stop/'}});
}]);

openDrglResources.factory('TripPatternStopResource', ['$resource', function($resource) {
    return $resource('/data/trip_pattern_stop/', {'pk': '@pk'}, {});
}]);

openDrglResources.factory('TripResource', ['$resource', function($resource) {
    return $resource('/data/trip/', {'pk': '@pk'}, {});
}]);

openDrglResources.factory('CalendarResource', ['$resource', function($resource) {
    return $resource('/data/calendars/:id', {'id': '@pk'}, {});
}]);
