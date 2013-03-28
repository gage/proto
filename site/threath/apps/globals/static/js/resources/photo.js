define([
    'jquery',
    'underscore', 
    'backbone',
    'utils/utils'
],  
function($, _, Backbone, Utils) {
    PhotoResource = {};
    PhotoResource.init = function($resource) {
        PhotoResource.Photo = $resource('/api/photos/:photoId',
            {photoId:'@id'}, {
            setting: {method:'POST', params:{charge:true}}
        });
    };
    return PhotoResource;
});