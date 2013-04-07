
app.directive('placeholder', ['$timeout', function($timeout){
    if (!BrowserDetect.browser == 'MSIE' || BrowserDetect.version >= 10) {
        return {};
    }
    return {
        link: function(scope, elm, attrs){
            if (attrs.type === 'password') {
                return;
            }
            $timeout(function(){
                elm.val(attrs.placeholder);
                elm[0].addEventListener('focus', function(e){
                    if(elm.val() == elm.attr('placeholder')){
                        elm.val('');
                    }
                });
                elm[0].addEventListener('blur', function(e){
                    if(elm.val() == ''){
                        elm.val(elm.attr('placeholder'));
                    }
                });
            });
        }
    }
}]);

app.directive('stopEvent', [function () {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            element.bind(attr.stopEvent, function (e) {
                e.stopPropagation();
            });
        }
    };
}]);

app.directive('body', function($rootScope){
    return {
        restrict: 'E',
        link: function(scope, element, attrs){
            element.ready(function(){
                element.removeClass('loading');
                $rootScope.$broadcast('bodyLoaded');
            });
        }
    }
});


// app.directive('flexbox', function ($timeout) {
//     if (!BrowserDetect.browser == 'MSIE' || BrowserDetect.version >= 10) {
//         return {};
//     };
//     return {
//         restrict: 'A',
//         link: function (scope, element, attr) {
//             var boxOptions = {
//                 target: element[0],
//                 orient: element[0].currentStyle['box-orient'] || "horizontal",
//                 align: element[0].currentStyle['box-align'] || "stretch",
//                 pack: element[0].currentStyle['box-pack'] || "start",
//                 direction: element[0].currentStyle['box-direction'] || "normal"
//             }
//             if(_.isArray(attr.flexbox)){
//                 options['flexMatrix'] = attr.flexbox;
//             };
//             $timeout(function(){
//                 var box = new Flexie.box(boxOptions);
//             });
//         }
//     };
// });


app.directive('scLightbox', ['$compile', '$templateCache', '$http', function($compile, $templateCache, $http){
    return{
        restrict: 'A',
        controller: function($scope, $element, $attrs){
            $scope.close = function(){
                $element.remove();
            }
        },
        template: '<div class=lightbox {[type]}>'+
                                 '<div class="lightboxBg" ng-click="close()" flexbox>'+
                                    '<div class="lightboxContent" stop-event="click"></div>'+
                                 '</div>'+
                             '</div>',
        link: function(scope, element, attrs){
            scope.type = 'text';
            function showLightbox(html){
                element.find('.lightboxContent').append($compile(html)(scope))
                element.children().css('display', 'block');

            }
            if(attrs.scLightbox){
                showLightbox(attrs.scLightbox);
            }else if(attrs.src){
                var cache = $templateCache.get(attrs.src);
                if($templateCache.get(attrs.src)){
                    if(typeof(cache) == 'string'){
                        showLightbox(cache);
                    }else{
                        showLightbox(cache[1]);
                    }
                }else{
                    $http.get(attrs.src, {cache:$templateCache}).success(function(){
                        showLightbox($templateCache.get(attrs.src)[1]);
                    });
                }
            }
        }
    }
}]);

app.directive('serverEmailValidate', ['$http', 'utils', 'errors', function($http, utils, errors) {
    return {
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl) {
            // If we use debounce, the return value will cause broken....
            function validate(viewValue) {
                if (!utils.validateEmail(viewValue)) {
                    // Not valid email
                    ctrl.$setValidity('duplicate', true);
                    ctrl.$setValidity('email', false);
                    return viewValue;
                }
                $http.get('/api/registration/check_email/?email='+viewValue).success(function(data, status, headers, config){
                    if (!data.success) {
                        if (data.error.code==errors.ERROR_REGISTRATION_EMAIL_USED) {
                            ctrl.$setValidity('duplicate', false);
                            ctrl.$setValidity('email', true);
                        }
                        else {
                            ctrl.$setValidity('email', false);
                            ctrl.$setValidity('duplicate', true);    
                        }
                    }
                    else {
                        ctrl.$setValidity('email', true);
                        ctrl.$setValidity('duplicate', true);
                    }
                });
                return viewValue;
            }
            var throttled = $.debounce(500, validate);

            ctrl.$parsers.unshift(validate);
        }
    };
}]);


app.directive("passwordVerify", function() {
    return {
        require: "ngModel",
        scope: {
            passwordVerify: '=',
            password: '='
        },
        link: function(scope, element, attrs, ctrl) {
            scope.$watch('password', function(value) {
                ctrl.$parsers.unshift(function(viewValue) {
                    var origin = scope.passwordVerify;
                    if (origin !== viewValue) {
                        ctrl.$setValidity("passwordVerify", false);
                        return viewValue;
                    } else {
                        ctrl.$setValidity("passwordVerify", true);
                        return viewValue;
                    }
                });
            });

        }
    };
});









