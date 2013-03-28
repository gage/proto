define(['jquery',
        'underscore', 
        'backbone'], 
function($,_,Backbone) {
    var Utils = {};

    //private
    var scope = new Backbone.Model();

    //public
    Utils.start = function(){ //init function
        scope.set({
        })
    };

    Utils.getScope = function(){
        return scope;
    };
    
    Utils.validateEmail = function(email){
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,4}))$/;
        return email.match(re);
    }

    Utils.htmlEncode = function(value){
        return $('<div/>').text(value).html();
    }

    Utils.redirect = function(url) {
        window.location = url;
    };

    Utils.start();
    return Utils;
});
