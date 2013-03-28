Site.Views.Landing = Site.Views.Landing || {};
var Landing = Landing || {};
Landing.Views = Landing.Views || {};

Landing.Views.loginForm = Backbone.View.extend({

    tagName: 'form',

    initialize: function(options){
        _.bindAll(this);
        this.required = options.required;
        this.booleans = options.booleans;
    },

    events: {
        'click .send': 'send',
        'click .remember_me': 'checkrmbme',
        'submit': 'submit'
    },

    _validate: function(){
        var _this = this;
        var data = this.$el.serializeObject();
        console.log(data);
        var valid = true;

        _.each(this.required, function(key){
            if(data[key] == '' || data[key] == undefined){
                _this.$('.'+key).data({
                    error: true,
                    message: gettext('This is required.')
                });
                valid = false;
            }
        });

        _.each(this.booleans, function(key){
            if(_this.$(key).attr('checked')){
                data[key] = true;
            }else{
                data[key] = false;
            }
        });

        if(valid)
            return data;
        else{
            return false;
        }
    },

    send: function(){
        var data = this._validate();
        if(data){
            $.ajax({
                url: '/api/auth/signin/',
                type: 'POST',
                data: data,
                success: function(r){
                    if(r.success){
                        debugger;
                        Utils.redirect('/');
                    }else{
                        console.log(r);
                    }
                },
                error: function(a,b,c){
                    console.log(a,b,c);
                }
            })
            return false;
        }else{
            return false;
        }
    },

    checkrmbme: function(){

    },

    submit: function(e){
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
});

$(function(){
    Site.Views.Landing.loginForm = new Landing.Views.loginForm({
        el: '#landing_content .login',
        required: ['username', 'password'],
        booleans: ['remember_me']
    });
});