define([
    'jquery',
    'underscore', 
    'backbone',
    'utils/utils'
],  
function($, _, Backbone, Utils) {
    UserResource = {};
    UserResource.init = function($resource) {
        UserResource.User = $resource('/api/user/:userId',
            {userId:'@id'}, {
            setting: {method:'POST', params:{charge:true}}
        });
    };
    return UserResource;
});