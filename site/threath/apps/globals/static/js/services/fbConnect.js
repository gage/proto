app.factory('fbConnect', [ function(){
    return function(cbk) {
        FB.login(function(response) {
            if(response.status == 'connected') {
                var data = {};
                var fbAccessToken = response.authResponse.accessToken;
                var facebookId = response.authResponse.userID;
                $.ajax({
                    url: '/api/facebook/connect/',
                    data: {
                        access_token: fbAccessToken,
                        facebook_id: facebookId
                    },
                    type: 'POST',
                    success: _.bind(function(r) {
                        if (r.success) {
                            window.location = "/";
                            return;
                        }
                        if(typeof cbk == 'function'){
                            cbk();
                        }
                    }, this),
                    error: _.bind(function(){
                        if(typeof cbk == 'function'){
                            cbk();
                        }
                    },this)
                });
            }
        }, {scope: 'user_likes,user_photos,user_birthday,email'});
}
}]);

