app.controller('bodyCtrl', ['$rootScope', '$scope', '$compile', 'currentUser', '$window', 
    function ($rootScope, $scope, $compile, currentUser, $window){
    
    $rootScope.appendLightbox = function(args, scope){
        // User can use "Parent Scope" or "Scope" to open new lightbox
        // set options
        var args = args || {};
        var options = {
            source: '',
            isTemplate: true,
            isDefer: false,
            level: 1,
            title:'',
            width:'',
            height:'',
            parentScope: $rootScope
        };
        angular.extend(options, args);
        
        var element = angular.element('<div lib-lightbox="lightboxOptions"></div>');
        element.appendTo($window.document.body);
        if (!scope) {
            scope = options.parentScope.$new();
        }
        
        scope.lightboxOptions = options;
        $compile(element)(scope);
        if(!scope.$root.$$phase) {
            scope.$apply();
        }
    };
    
}]);


app.controller('lightboxFrameCtrl',['$scope','$window', function($scope, $window){
    
    // console.log($scope.lightboxOptions)
    $scope.lightboxFrameOptions = {
        title: $scope.lightboxOptions.title,
        style:{}
    };
    // $scope.lightboxFrameTitle = $scope.lightboxOptions.title;
    // $scope.lightboxFrameStyle = {};
    if($scope.lightboxOptions.width){
        $scope.lightboxFrameOptions.style.width = $scope.lightboxOptions.width;
    }
    if($scope.lightboxOptions.height){
        $scope.lightboxFrameOptions.style.height = $scope.lightboxOptions.height;
    }

    $scope.setDefaultTitle = function(title){
        if (!$scope.lightboxFrameOptions.title) {
            $scope.lightboxFrameOptions.title = title;
        }
    };

    $scope.setDefaultWidth = function(width){
        if (!$scope.lightboxFrameOptions.style.width) {
            $scope.lightboxFrameOptions.style.width = width;
        }
    };
}]);
