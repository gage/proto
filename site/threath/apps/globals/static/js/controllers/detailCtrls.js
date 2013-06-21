app.controller('detailCtrls.window', ['$rootScope', '$scope', '$compile', 'currentUser', 'utils', function ($rootScope, $scope, $compile, currentUser, utils){
	// Should define these parameter before open lightbox
	// $scope.iframeUrl, apiPrefix, iframeObj
}]);


app.controller('detailCtrls.image', ['$rootScope', '$scope', '$compile', 'currentUser', 'utils', function ($rootScope, $scope, $compile, currentUser, utils){
	$scope.showMagnify = false;
	$scope.openInNewTab = function(){
		utils.openInNewTab($scope.lightboxImg.original_raw);
	}
    
}]);

