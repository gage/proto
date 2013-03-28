require.config({
    baseUrl: '/static/js/',
    paths: {
        lib: 'lib',
        jquery: 'lib/jquery-min',
        backbone: 'lib/backbone-min',
        underscore: 'lib/underscore-min',
        angular:  'lib/angular',
        angular_resource:  'lib/angular-resource.min',
        less: 'lib/less',
        css_root: '../css'
    },
    shim: {
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        underscore: {
            exports: '_'
        },
        angular: {
            exports: 'angular'
        },
        angular_resource: {
            deps: ['angular'],
            exports: 'angular_resource'
        },   
    },
    map: {
        '*': {
            'css': 'lib/require-css/css'
        }
    }
});

requirejs([
    'jquery',
    'underscore', 
    'backbone',
    'angular',
    'initData',
    'ctrls',
    'utils/utils',
    'photo_gallery/photo_gallery',

    'controllers/routeCtrls',

    'resources/user',

    'apps/all',

    'angular_resource',
    'css'
], function ($ , _, Backbone, angular, InitData, Ctrls, Utils, PhotoGallery, 
        routeCtrls,
        UserResource,
        Apps
    ){
    //jQuery, underscore, and backbone are
    //loaded and can be used here now.

    Ctrls.Route = routeCtrls;

    // Hook on controllers
    _.each(Apps, function(appObj){
        Ctrls[appObj.scopeName] = appObj.controllers;
    });

    angular.element(document).ready(function() {
        var app = angular.module("app", ['ngResource'], function($routeProvider, $locationProvider){

            // Define the url routing
            $locationProvider.html5Mode(true);
            $routeProvider
                .when('/', 
                {
                    controller: "Ctrls.Route.IndexCtrl",
                    templateUrl: 'agl_index_page.html'
                })
                .when('/user/:userId/', 
                {
                    controller: "Ctrls.Route.IndexCtrl",
                    templateUrl: 'agl_index_page.html'
                })
                .when('/landing/',
                {
                    controller: "Ctrls.Route.LandingCtrl",
                    templateUrl: 'agl_landing_page.html'
                })
                .otherwise({
                    template: 'This does not exist.'
                });
        });

        // Changet the syntex
        app.config(function($interpolateProvider) {
            $interpolateProvider.startSymbol('{[');
            $interpolateProvider.endSymbol(']}');
        });

        // Hang-on Directives
        _.each(Apps, function(appObj){
            $.each(appObj.directives, function(name, func){
                app.directive(name, func);
            });
        });

        // Bootstrap Angular JS
        angular.bootstrap(document, ['app']);
    });

    BigPipe.start();
    console.log('JS requirement loaded');
    var photoCollection = new PhotoGallery.PhotoCollection(InitData.photoCollection);
    // console.log(new Backbone.Collection(InitData.photoCollection));
});

