app.controller('signupCtrl', ['$scope', 'fbConnect', '$http', 'errors', function ($scope, fbConnect, $http, errors){
    $scope.formData = {email: '', password:'', passwordConfirm: ''};
    $scope.afterSubmit = false;
    $scope.sending = false;
    $scope.completeSubmit = false;
    $scope.fbConnecting = false;

    // Hookon service
    $scope.errors = errors;
    $scope.errCode = errors.ERROR_GENERAL_NO_ERROR;
    $scope.regObj = {user_id: "", id: "", created: ""};
    
    var elm = $('#signupForm .field input');
    elm.bind('keydown', function() {
        $scope.afterSubmit = false;
        $scope.errCode = errors.ERROR_GENERAL_NO_ERROR;
    });

    $scope.submit = function() {
        $scope.afterSubmit = true;
        if (!$scope.signupForm.$valid){return;}
        var f = $scope.formData;
        $scope.sending = true;
        $http.post("/api/registration/signup/", {"email": f.email, "password": f.password, "password_confirm": f.passwordConfirm})
        .success(function(data, status){
            $scope.sending = false;
            if (!data.success) {
                var errorList = [
                    errors.ERROR_AUTH_PASSWORD_CONFIRM_NOT_MATCH, errors.ERROR_AUTH_PASSWORD_INVALID,
                    errors.ERROR_AUTH_USER_ALREADY_LOGIN
                ];
                var code = data.error.code;
                if (_.contains(errorList, code)) {
                    $scope.errCode = code;
                    if (code==errors.ERROR_AUTH_USER_ALREADY_LOGIN) {
                        window.location = "/";
                        return;    
                    }
                }
                else {
                    console.error('Should implement this error ' + code);
                }
            }
            else {
                $scope.completeSubmit = true;
                $scope.regObj = data.response;
            }
        })
        .error(function(){
            $scope.sending = false;
        });
    }

    $scope.resend = function() {
        $scope.sending = true;
        $http.post("/api/registration/resend_account_activation_code/", {"registration_id": $scope.regObj.id})
        .success(function(data, status){
            $scope.sending = false;
        })
        .error(function(){
            $scope.sending = false;
        });
    }

    $scope.fbConnect = function() {
        if($scope.fbConnecting) {return;}
        $scope.fbConnecting = true;
        fbConnect(function(){
            $scope.fbConnecting = false;
        });
    };

}]);


app.controller('loginCtrl', ['$scope', '$routeParams', '$http', 'errors', 'fbConnect', function ($scope, $routeParams, $http, errors, fbConnect){
    
    $scope.formData = {user_identity: '', password:''};
    $scope.sending = false;
    $scope.completeSubmit = false;
    $scope.onResendMode = false;
    $scope.fbConnecting = false;

    // Hookon service
    $scope.errors = errors;
    $scope.errCode = errors.ERROR_GENERAL_NO_ERROR;

    if ($routeParams.mode=='resend') {
        $scope.onResendMode = true;
    }

    var elm = $('#loginForm .field input');
    elm.bind('keydown', function() {
        $scope.errCode = errors.ERROR_GENERAL_NO_ERROR;
    });

    $scope.submit = function() {
        // This is a hack for the chrome or firefox initial data...
        if ($scope.loginForm.userId.$viewValue==undefined) {
            $scope.formData.user_identity = $('#loginForm .id-wrap input').val();
        }
        if ($scope.loginForm.password.$viewValue==undefined) {
            $scope.formData.password = $('#loginForm .password-wrap input').val();
        }

        var f = $scope.loginForm;
        $scope.sending = true;

        $http.post("/api/auth/general_signin/", $scope.formData)
        .success(function(data, status){
            if (!data.success) {
                var errorList = [
                    errors.ERROR_USER_PASSWORD_NOT_MATCH, errors.ERROR_REGISTRATION_NOT_REGIST_YET,
                    errors.ERROR_REGISTRATION_NOT_ACTIVATE, errors.ERROR_AUTH_USER_ALREADY_LOGIN
                ];
                var code = data.error.code;
                if (_.contains(errorList, code)) {
                    $scope.errCode = code;
                    if (code==errors.ERROR_AUTH_USER_ALREADY_LOGIN) {
                        window.location = "/";
                        return;    
                    }
                }
                else {
                    console.error('Should implement this error ' + code);
                }
            }
            else {
                $scope.completeSubmit = true;
                window.location = "/";
                return;
            }
            $scope.sending = false;
        })
        .error(function(){
            $scope.sending = false;
        });
    }

    $scope.fbConnect = function() {
        if($scope.fbConnecting){return;}
        $scope.fbConnecting = true;
        fbConnect(function(){
            $scope.fbConnecting = false;
        });
    };

}]);


app.controller('resendEmailCtrl', ['$scope', '$location', '$http', 'errors', function ($scope, $location, $http, errors){
    $scope.formData = {email: ''};
    $scope.sending = false;
    $scope.completeSubmit = false;

    // Hookon service
    $scope.errors = errors;
    $scope.errCode = errors.ERROR_GENERAL_NO_ERROR;

    var elm = $('#resendForm .field input');
    elm.bind('keydown', function() {
        $scope.errCode = errors.ERROR_GENERAL_NO_ERROR;
    });

    $scope.resend = function() {
        var f = $scope.resendForm;
        $scope.sending = true;

        $http.post("/api/registration/send_forget_password_email/", $scope.formData)
        .success(function(data, status){
            if (!data.success) {
                var errorList = [errors.ERROR_GENERAL_USER_NOT_FOUND];
                var code = data.error.code;
                if (_.contains(errorList, code)) {
                    $scope.errCode = code;
                }
                else {
                    console.error('Should implement this error ' + code);
                }
            }
            else {
                $scope.completeSubmit = true;
                // window.location = "/";
                return;
            }
            $scope.sending = false;
        })
        .error(function(){
            $scope.sending = false;
        });
    }

}]);

