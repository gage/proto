app.factory('geoLocation', ['$q','$http','$timeout',function($q,$http,$timeout){
    geoLocation = {};
    geoLocation.latlon = [];
    geoLocation.country_code = '';

    geoLocation.getLatlon = function(){
        return geoLocation.latlon;
    };

    geoLocation.requestLatlon = function(){
        var deferred = $q.defer();
        if (navigator.geolocation){
            navigator.geolocation.getCurrentPosition(function(position){
                deferred.resolve([position.coords.latitude, position.coords.longitude]);
            }, function(){}, {timeout:10000, enableHighAccuracy: true, maximumAge: 60000});
        }else{
            deferred.reject();
        }
        return deferred.promise;
    };

    geoLocation.checkHtml5Location = function(){
        geoLocation.requestLatlon().then(function(resolved){
            geoLocation.latlon[0] = resolved[0];
            geoLocation.latlon[1] = resolved[1];
        }); 
    }

    geoLocation.checkHtml5Location();

    return geoLocation;
}]);





