app.directive('scBoxParent', [function () {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        scope:true,
        template: '<div class="scBoxParent" ng-transclude></div>'

    }
}]);


app.directive('scBox', [function () {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        template: '<div class="scBox"><div class="scBoxInnerWrap" ng-transclude></div></div>'

    };
}]);







