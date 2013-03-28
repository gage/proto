define(['jquery',
		'underscore', 
        'backbone',
        'utils/utils',
        'initData',
        'resources/photo'
        ],	
function($, _, Backbone, Utils, InitData, PhotoResource) {
var PhotoApp = {};

// For Scope
PhotoApp.scopeName = 'Photo';

PhotoApp.controllers = {
    PhotoCtrl : function ($scope, $resource) {
    	PhotoResource.init($resource);
    	$scope.photos = PhotoResource.Photo.query({raw:true}, function(){
    	});

	    $scope.addPhoto = function() {
		    this.photos.push({original_raw:'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash4/274184_702945634_1610966595_q.jpg'});
		};
	}
};

PhotoApp.directives = {
};

return PhotoApp;

});
