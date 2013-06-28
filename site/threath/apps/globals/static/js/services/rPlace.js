app.factory('rPlace', ['$remoteData', '$http', '$q', 'geoLocation', 'utils',  function($remoteData, $http, $q, geoLocation, utils){

    var latlon = geoLocation.getLatlon();

    var foursquareData = $remoteData({
        url:'/api/place/fs/'
    });
    
    foursquareData.getData = function(para){
        var deferred = $q.defer();
        var options = {
            latlon: latlon
        }
        // q, radius
        _.extend(options, para);
        var query = options.query;

        if(!options.latlon.length){
            deferred.reject('no geolocation info');
            return deferred.promise;
        }
        var latlonStr = options.latlon[0]+','+options.latlon[1];

        options.latlon = latlonStr;
        var para = utils.serialize(options);
        var queryUrl = '/api/place/fs/explore/?'+para;
        
        $http.get(queryUrl)
        .success(function(data, status, headers, config){
            var list = foursquareData.initCollection({
                models: data.response
            });
            deferred.resolve(list);
        })
        .error(function(data, status, headers, config){
            var errmsg = '';
            deferred.reject(errmsg);
        });
        return deferred.promise;
    };
    
    foursquareData.getObj = function(id){
        var deferred = $q.defer();
        var queryUrl = '/api/place/fs/'+id+'/?detail=true';
        $http.get(queryUrl)
        .success(function(data, status, headers, config){
            deferred.resolve(data.response);
        })
        .error(function(data, status, headers, config){
            var errmsg = '';
            deferred.reject(errmsg);
        });
        return deferred.promise;
    }

    return foursquareData;
    
    
}]);


