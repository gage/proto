define(['jquery',
		'underscore', 
        'backbone',
        'utils/utils',
        'initData',
        'resources/user'
        ],	
function($, _, Backbone, Utils, InitData, UserResource) {
var UserApp = {};

UserApp.scopeName = 'User';

UserApp.controllers = {

	UserCtrl : function($scope, $http, $resource, $routeParams) {
		UserResource.init($resource);
		$scope.template = {url: '/static/html/agl_landing_page.html'};
		$scope.users = UserResource.User.query({raw:true}, function(){
			_.each($scope.users, function(user){
				if (user.id==$routeParams.userId) {
					user.class = "selected";
				}
			});
		});
		$scope.changeUrl = function() {
			$scope.template.url = '/static/html/agl_main_page.html';
		}
		$scope.tip = function() {
			console.log('show tip');
		}
	},

	TabCtrl: function($scope, $http, $resource, $routeParams) {
		$scope.tabs = [{name: 'Tab1', content: 'Tab1 content blah'}, {name:'Tab2', content: 'Tab2 lala'}];
		$scope.tabContent = '';
		$scope.changeContent = function(tab) {
			$scope.tabContent = tab.content;
		}
	}
};

UserApp.directives = {
	userInfo : function() {
		return {
			link: function(scope, element, attrs) {
				element.bind('mouseenter', function(){
					console.log('popout', attrs.userInfo);
					scope.$parent.tip();
					// console.log(attrs.tip);
					// attrs.tip();
				})
			},
			restrict: 'A'
		}
	}
};

return UserApp;

});
