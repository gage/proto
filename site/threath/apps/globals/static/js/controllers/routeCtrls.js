define(['jquery',
		'underscore', 
        'backbone',
        'utils/utils',
        'initData',
        'resources/user'
        ],	
function($, _, Backbone, Utils, InitData, UserResource) {
var controllers = {
	LandingCtrl : function($scope, $routeParams) {
		// console.warn('landing');
	},
	IndexCtrl: function($scope, $routeParams) {
		// console.warn('index', $routeParams);
	}
};
return controllers;

});
