app.controller('bodyCtrl', ['$scope', '$compile', 'currentUser', function ($scope, $compile, currentUser){
    
    $scope.insertLightbox = function(source, isTemplate){
        var elStr = '';
        if(isTemplate){
            elStr = '<div sc-lightbox src="'+source+'"></div>'
        }else{
            elStr = '<div sc-lightbox="'+source+'"></div>'
        }
        var el = angular.element(elStr);
        el.appendTo(document.body);
        $compile(el)($scope)
    };

    
    
}])
