app.controller('chatColCtrl', ['$scope', 'currentUser', 'chatRoom', 'utils', '$rootScope', function ($scope, currentUser, chatRoom, utils, $rootScope){
    $scope.model = currentUser.model;
    $scope.searchKey = '';
    $scope.loading = true;
    var chatroomsPromise = chatRoom.query().then(function(resolved){
        $scope.chatRooms = resolved.list;
        $scope.loading = false;
        $scope.isEmpty = $scope.chatRooms == 0;
        if($scope.chatRooms.length>0){
            $rootScope.currentRoom = $scope.chatRooms[0];    
        }
        

    }, function(errmsg){
        console.log(errmsg);
        $scope.loading = false;
    });

    $scope.$watch('searchKey', function(newVal, oldVal){
        if(!newVal){
            _.each($scope.chatRooms, function(room){
                room.isHide = false;
            });
        }else{
            _.each($scope.chatRooms, function(room){
                if(!room.name.sequenceMatch(newVal)){
                    room.isHide = true;    
                }
            });
        }
    });
}]);

app.controller('chatItemCtrl', ['$scope', '$rootScope',  function ($scope, $rootScope){
    $rootScope.$watch('currentRoom', function(newVal, oldVal){
        if(!newVal){
            return;
        }
        if(newVal.id == $scope.room.id){
            $scope.active = true;        
        }else{
            $scope.active = false;       
        }
    })

    $scope.slectRoom = function(){
        $rootScope.currentRoom = $scope.room;
    }
    $scope.deleteChatRoom = function(){
        $scope.room.remove();
    }
}]);    







