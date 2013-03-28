define(['jquery',
        'underscore', 
        'backbone'], 
function($,_,Backbone) {
    var InitData = {};

    //private
    var scope = new Backbone.Model();

    //public
    InitData.exampleFun = function(a, b){
        return a*b;
    };

    InitData.start = function(){ //init function
        console.log('start InitData');
        scope.set({
            aaa:5,
            bbb:3
        })
    };

    InitData.getScope = function(){
        return scope;
    };
    


    InitData.start();
    return InitData;
});
