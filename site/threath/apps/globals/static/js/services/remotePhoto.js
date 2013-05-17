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

    var modelProto = {
        available: true,
        getUrl: function(){
            if (this.available) {
                return this.original_raw;    
            }
            else {
                return '';
            }
            
        }
    };
    _.extend(remotePhoto.prototype,  modelProto);

    var collectionProto = {
    };
    _.extend(remotePhoto.collection.prototype,  collectionProto);

    return remotePhoto;
}]);


