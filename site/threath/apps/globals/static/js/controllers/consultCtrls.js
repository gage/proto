app.controller('consultCtrls.list', ['$scope', '$rootScope', 'remoteConsult', function ($scope, $rootScope, remoteConsult){
    $scope.consultList = remoteConsult.initCollection();
    $scope.consultList.fetch().then(function(resolved){
    	$scope.consultList = resolved;
    }, function(errmsg){
    	console.log('error');	
    });
}]); 