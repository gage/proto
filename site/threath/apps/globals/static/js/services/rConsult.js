app.factory('rConsult', ['$remoteData', function($remoteData){
    
    var rConsult = $remoteData({
        url: '/api/user/',
        parse: function(response){
            return response.response;
        },
        comparator: function(obj){
            return obj.full_name;
        }
    });

    rConsult.loadMore = function(){
    };

    rConsult.prototype.getThing = function(){
        return '';
    };


    return rConsult;
}]);


