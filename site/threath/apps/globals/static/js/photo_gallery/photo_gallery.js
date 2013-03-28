// Pages Module

define(['jquery',
        'underscore', 
        'backbone',
        'utils/utils'
        ], 
function($, _, Backbone, Utils) {
    var PhotoGallery = {},
        scope = new Backbone.Model({
            rootUrl: ''
        });


    //public
    PhotoGallery.exampleFun = function(a, b){
        return a+b;
    };
    
    PhotoGallery.start = function(){ //init function
        console.log('start PhotoGallery')
       
    };

    PhotoGallery.PhotoModel = Backbone.Model.extend({
        defaults: {
            url: ''
        }
    });

    PhotoGallery.PhotoCollection = Backbone.Collection.extend({
        model: PhotoGallery.PhotoModel,
        comparator: function(model){
            return 1;
        },
        parse: function(response){
            if (response.response) {
                return response.response;
            }
            return response;
        },
        url: function(){
            return '';
        }
    });

    PhotoGallery.PageView = Backbone.View.extend({
        
    });

    PhotoGallery.PhotoCtrl = function ($scope) {
        $scope.todos = InitData.photoCollection;
    };

    PhotoGallery.start();
    return PhotoGallery;
});
