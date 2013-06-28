var app = angular.module("sc", ['remoteData', 'ui', 'ui.bootstrap', 'ui.select2', 'ui.state']);

app.config(['$urlRouterProvider', '$stateProvider', '$locationProvider', '$interpolateProvider', 
    function($urlRouterProvider, $stateProvider, $locationProvider, $interpolateProvider){
    $locationProvider.html5Mode(true);

    // Changet the syntex
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');

    $stateProvider
        .state('main',{
            url: "/",
            templateUrl: "index.html",
            onEnter: function(){
                console.log('on main');
            }
        })
        .state('main.sideBarA',{
            url: "^/sidebar/A",
            views: {
                'sidebar': {
                    templateUrl: "sidebarA.html"
                },
                'sidebarSub': {
                    templateUrl: "sidebarSubA.html"
                }
            },
            onEnter: function(){
                console.log('on A');
            }
        })
        .state('main.sideBarB',{
            url: "^/sidebar/B",
            views: {
                'sidebar': {
                    templateUrl: "sidebarB.html" 
                },
                'sidebarSub': {
                    templateUrl: "sidebarSubB.html"
                }

            }
        })
       .state('test',{
           url: "/test",
           template: "<h1 ng-controller='testCtrl'>This is a test page</h1>"
       })
       .state('test.num',{
           url: "/{id}",
           template: "<h1>This will not show, child state will not render template.</h1>"
       })
       .state('test.another',{
        // Absolute Url
           url: "^/list",
           template: "<h1>This will not show, child state will not render template.</h1>"
       })
       .state('othertest',{
           url: "/test/another/rule",
           template: "<h1>other test</h1>"
       })
       .state('logout', {
           url: "/logout",
           onEnter: function(){
             window.location = '/logout';
           }
       })
        .state('errors',{
            url: "/page_not_found",
            templateUrl: "/static/html/page_not_found.html",
            onEnter: function(){
                // alert('enter')
            },
            onExit: function(){
                // alert('leave')
            }
        });

    $urlRouterProvider.otherwise('/page_not_found');
}]);

// app.run(['$rootScope', '$state', '$stateParams', function($rootScope, $state, $stateParams){
//     // Not working yet... ui-sref
//     $rootScope.$state = $state;
//     $rootScope.$stateParams = $stateParams;
// }])

app.controller('testCtrl', ['$state', '$stateParams', function($state, $stateParams){
    console.log($stateParams);
}])
