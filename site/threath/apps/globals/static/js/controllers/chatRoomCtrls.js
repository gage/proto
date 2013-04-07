app.controller('chatRoomCtrl', ['$scope', '$rootScope',  function ($scope, $rootScope){
    $rootScope.$watch('currentRoom', function(newVal, oldVal){
        if(!newVal){
            $scope.hasRoom = false;
        }else{
            $scope.hasRoom = true;
        }
    })
}]);    

app.controller('messageListCtrl', ['$scope', '$rootScope',  function ($scope, $rootScope){
    
}]);    
