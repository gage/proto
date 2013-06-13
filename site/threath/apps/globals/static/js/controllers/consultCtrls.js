app.controller('consultCtrls.list', ['$scope', '$rootScope', 'rConsult', function ($scope, $rootScope, rConsult){
    $scope.consultList = rConsult.initCollection();
    $scope.consultList.fetch().then(function(resolved){
    	$scope.consultList = resolved;
    }, function(errmsg){
    	console.log('error');	
    });
}]); 