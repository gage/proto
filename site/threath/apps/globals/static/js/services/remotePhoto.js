app.factory('remotePhoto', ['$remoteData', function($remoteData){
    
    var remotePhoto = $remoteData({
        url: '/api/photos/',
        parse: function(response){
            return response.response;
        },
        comparator: function(obj){
            return obj.updated;
        }
    });

    remotePhoto.loadMore = function(){
    };

    remotePhoto.prototype.getUrl = function(){
        console.log(this.original_raw);
        return this.original_raw;
    };


    


    return remotePhoto;
}]);


