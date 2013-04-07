var app = angular.module("sc", ['remoteData']);

app.config(function($routeProvider, $locationProvider, $interpolateProvider){
    $locationProvider.html5Mode(true);

    // Changet the syntex
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');

    $routeProvider
        .when('/',
        {
            templateUrl: "index.html",
        })
        .otherwise({
            templateUrl: "/static/html/page_not_found.html",
        })
});


