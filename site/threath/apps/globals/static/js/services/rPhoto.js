app.factory('rPhoto', ['$remoteData', function($remoteData){
    
    var rPhoto = $remoteData({
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
    _.extend(rPhoto.prototype,  modelProto);

    var collectionProto = {
    };
    _.extend(rPhoto.collection.prototype,  collectionProto);

    return rPhoto;
}]);


