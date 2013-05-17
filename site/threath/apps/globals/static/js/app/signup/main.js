var app = angular.module("scSignup", []);

app.config(function($routeProvider, $locationProvider, $interpolateProvider){
	var appRoot = '/signup/';
    $locationProvider.html5Mode(true);
    // Changet the syntex
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    var handleRoot = {
        redirectTo: function (routeParams, path, search) {
            // Redirect to other app
            window.location = '/';
        } 
    };

    if(BrowserDetect.browser == 'MSIE' || BrowserDetect.browser == 'Explorer'){
        handleRoot = {
            redirectTo: function (routeParams, path, search) {
                // Redirect to other app
                window.location = '/?landing=true';
            }
        };
    }

    $routeProvider
        .when('',
            handleRoot
        )
        .when('/',
            handleRoot
        )
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


