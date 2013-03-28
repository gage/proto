define(['jquery',
		'underscore', 
        'backbone',
        'utils/utils',
        ],	
function($, _, Backbone, Utils){
var GlobalApp = {};

// For Scope
GlobalApp.scopeName = 'Global';

GlobalApp.controllers = {
    Ctrl : function ($scope, $resource) {
	}
};

GlobalApp.directives = {
};

return GlobalApp;

});
