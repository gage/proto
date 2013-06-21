app.factory('rSoundcloud', ['$remoteData', '$http', '$q', 'utils',  function($remoteData, $http, $q, utils){

    var soundcloudData = $remoteData({
        parse: function(response){
            return response.response;
        },
        url: function(){
            return '/api/soundcloud/top/';
        }
    });

    var soundcloudCollection = soundcloudData.getCollectionClass();
    
    soundcloudCollection.prototype.getData = function(para){
        var deferred = $q.defer();
        var options = {
            q: ''
        }
        _.extend(options, para);

        this.mode = options.q=='' ? 'top': 'search';
        return this.fetch(options);
    };

    soundcloudCollection.prototype.url = function(){
        if (this.mode=='search') {
            return '/api/soundcloud/search/';
        }
        else {
            return '/api/soundcloud/top/';
        }
    };
    
    // soundcloudData.prototype.getObj = function(id){
    //     var deferred = $q.defer();
    //     var queryUrl = '/api/place/fs/'+id+'/?detail=true';
    //     $http.get(queryUrl)
    //     .success(function(data, status, headers, config){
    //         deferred.resolve(data.response);
    //     })
    //     .error(function(data, status, headers, config){
    //         var errmsg = '';
    //         deferred.reject(errmsg);
    //     });
    //     return deferred.promise;
    // }

    return soundcloudData;
    
    
}]);


