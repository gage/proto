define(['jquery',
		'underscore', 
        'backbone',
        'utils/utils',

        'apps/user',
        'apps/photo',
        'apps/global'
        ],
function($, _, Backbone, Utils, UserApp, PhotoApp, GlobalApp) {
var Apps = [UserApp, PhotoApp, GlobalApp];

return Apps;
});
