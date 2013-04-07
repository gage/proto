var app = angular.module("scSignup", []);

app.config(function($routeProvider, $locationProvider, $interpolateProvider){
	var appRoot = '/signup';
    $locationProvider.html5Mode(true);
    // Changet the syntex
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    $routeProvider
        .when(appRoot,
        {
            templateUrl: "signup_tpl.html"
        })
        .when("/login",
        {
            templateUrl: "login_tpl.html"
        })
        .when("/login/:mode",
        {
            templateUrl: "login_tpl.html"
        })
        .when(appRoot+'/test',
        {
            templateUrl: "test_tpl.html"
        }) 
        .when(appRoot+'/:anything', {
            templateUrl: "/static/html/page_not_found.html"
        })
        .otherwise({
            redirectTo: function (routeParams, path, search) {
                // Redirect to other app
            	window.location = window.location.href;
            } 
        })
});


