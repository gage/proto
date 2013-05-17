app.factory('remoteConsult', ['$remoteData', function($remoteData){
    
    var remoteConsult = $remoteData({
        url: '/api/user/',
        parse: function(response){
            return response.response;
        },
        comparator: function(obj){
            return obj.full_name;
        }
    });

    remoteConsult.loadMore = function(){
    };

    remoteConsult.prototype.getThing = function(){
        return '';
    };


    return remoteConsult;
}]);


