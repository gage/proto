app.factory('chatRoom', ['$remoteData', function($remoteData){
    
    var chatRoom = $remoteData({
        url: '/api/chatroom/',
        parse: function(response){
            return response.response;
        },
        comparator: function(obj){
            return obj.updated;
        }
    });

    chatRoom.loadMore = function(chatRoomList){
        console.log('www')
    };

    chatRoom.prototype.mute = function(){
        console.log('kkk')
    };
    
    chatRoom.prototype.block = function(){

    };

    chatRoom.prototype.remove = function(){
        alert('please implement')
    };


    


    return chatRoom;
}]);


