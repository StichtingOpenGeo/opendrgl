/**
 * Created by Joel Haasnoot on 26/12/14.
 */

var openDrglUtils = angular.module('openDrglUtils', []);

openDrglUtils.service('StringUtils', function() {

    this.splitChbId = function(id) {
        var splitString = id.split(':');
        if (splitString.length == 3) {
            return splitString[2];
        } else {
            return splitString[0];
        }
    }


});

openDrglUtils.service('MathUtils', function() {

    this.getMaxOrder = function(arr) {
        var highest = -1;
        for (var key in arr) {
            var numOrder = parseInt(arr[key].order)
            if (numOrder > highest) {
                highest = numOrder;
            }
        }
        return highest
    }

});

openDrglUtils.service('TimeUtils', function() {

    this.parseTime = function(input) {
        if (input == null) {
            return null;
        }
        var out = new Date();
        var split = input.split(':');
        out.setHours(parseInt(split[0]));
        if (split.length > 1 && split[1] != "") {
            out.setMinutes(parseInt(split[1]));
        } else {
            out.setMinutes(0);
        }
        if (split.length > 2 && split[2] != "") {
            out.setSeconds(parseInt(split[2]));
        } else {
            out.setSeconds(0);
        }
        return out;
    }

    this.parseTimeToSeconds = function(input) {
        if (input == null) {
            return null;
        }
        var split = input.split(':');
        var out = parseInt(split[0]) * 60*60;
        if (split.length > 1 && split[1] != "") {
            out += parseInt(split[1]) * 60;
        }
        if (split.length > 2 && split[2] != "") {
            out += parseInt(split[2]);
        }
        return out;
    }

    this.padTime = function(input) {
        if (input < 10) {
            return "0" + input;
        }
        return input
    }

    this.printTime = function(time) {
        if (time == null) {
            return "--:--:--";
        }
        return this.padTime(time.getHours())+":"+this.padTime(time.getMinutes())+":"+this.padTime(time.getSeconds());
    }

    this.parseSeconds = function (baseSeconds) {
        var time = new Date();
        var hours   = Math.floor(baseSeconds / 3600);
        var minutes = Math.floor((baseSeconds - (hours * 3600)) / 60);
        time.setHours(hours, minutes, baseSeconds - (hours * 3600) - (minutes * 60))
        return time
    };

    this.printSeconds = function(seconds) {
        return this.printTime(this.parseSeconds(seconds));
    }

    this.parseDateToSeconds = function(date) {
        return date.getSeconds() + date.getMinutes() * 60 + date.getHours() * 60 * 60;
    }

});

openDrglUtils.service('ArrayUtils', function() {

    this.uniqueDicts = function(array, key) {
        var a = array.concat();
        for(var i=0; i<a.length; ++i) {
            for(var j=i+1; j<a.length; ++j) {
                if(a[i][key] === a[j][key])
                    a.splice(j--, 1);
            }
        }

        return a;
    };

    this.sortByKey = function(array, key) {
        return array.sort(function(a, b) {
            var x = a[key]; var y = b[key];
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        });
    }

});