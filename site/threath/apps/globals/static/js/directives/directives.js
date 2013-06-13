app.directive('eventListener', function(){ 
   return {
      restrict: 'A', 
      link: function(scope, elem, attrs) {

        var options = {
            callback: function(){
                console.log('Warning for non-define event listener');
            },
            name: 'focus'
        }

        var args = scope.$eval(attrs.eventListener);
        if (!angular.isArray(args)) {
            args = [args];
        }

        function _bindEvent(opt){
            var _opt = {};
            _.extend(_opt,  options);
            _.extend(_opt,  opt);
            elem.bind(_opt.name, _opt.callback);
        }

        _.each(args, function(para){
            _bindEvent(para);
        });
      }
   };
});


app.directive('gglSuggest', ['$timeout',function ($timeout) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var language = window.navigator.userLanguage || window.navigator.language;
            var options = {
                type: 'google',
                cbk: function(){}
            }

            var cOpt = scope.$eval(attrs.gglSuggest);
            _.extend(options, cOpt);
            var suggestType = options.type;

            var modelName = attrs.ngModel;
            function assignNgModel(val){
                scope[modelName] = val;
            }
            $(element).bind('autocompleteselect', function(e, ui){
                // Assign select value to input model
                assignNgModel(ui.item.value);
                options.cbk(e, ui);
            })

            $(element).autocomplete({
                source: function(request, response) {
                    assignNgModel(request.term);
                    if (suggestType == 'map') {
                        var service = new google.maps.places.AutocompleteService();
                        service.getQueryPredictions({input: request.term}, function(predictions){
                            var suggestions = [];
                            _.each(predictions, function(val){
                                suggestions.push({value: val.description});
                            });
                            response(suggestions);
                        });
                    }
                    else {
                        $.getJSON("http://suggestqueries.google.com/complete/search?callback=?",
                            { 
                              "hl":language, // Language
                              // "ds":"yt", // Restrict lookup to youtube
                              "jsonp":"suggestCallBack", // jsonp callback function name
                              "q":request.term, // query term
                              "client":"youtube" // force youtube style response, i.e. jsonp
                            }
                        );
                        // Global...
                        suggestCallBack = function (data) {
                            var suggestions = [];
                            $.each(data[1], function(key, val) {
                                suggestions.push({"value":val[0]});
                            });
                            suggestions.length = 5; // prune suggestions list to only 5 items
                            response(suggestions);
                        };
                    }
                },
            });
        }
    };
}]);


app.directive('focusScrollTo', ['$timeout',function ($timeout) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            // select2-focus
            // TODO: change the scroll target
            var options = {
                target: 'html, body',
                offset: 0,
                eventName: 'focus'
            };
            var cOpt = scope.$eval(attrs.focusScrollTo);
            _.extend(options,  cOpt);
            $(element).bind(options.eventName, function(){
                $(options.target).animate({
                    scrollTop: $(element).offset().top + parseFloat(options.offset)
                }, 500);
            });

        }
    };
}]);

// From others

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

app.directive('img', [function(){
    return {
        restrict: 'E',
        link: function(scope, element, attrs){
            var defaultImg = '/static/images/blank.png';
            
            var $img = $(element);
            $img.error(function(e){
                var apply = function(){
                    if (attrs.defaultImg) {
                        defaultImg = attrs.defaultImg;
                    }
                    // if ($(e.target).attr('ng-src')) {
                    //     $(e.target).attr('ng-src', defaultImg);
                    // }
                    $(e.target).attr('src', defaultImg);
                };
                if(!scope.$root.$$phase) {
                    scope.$apply(apply);
                }
                else {
                    apply();
                }
                
            });
        }
    }
}]);


app.directive('loadingImg', [function(){
    return {
        restrict: 'A',
        link: function(scope, element, attrs){
            // var loadingImg = attrs.loadingImg;
            var defaultImg = '/static/images/transparent.png';

            var args = scope.$eval(attrs.loadingImg);
            var options = {
                cls: '',
                transition: true
            };
            _.extend(options, args);
            

            var hasLoaded = false;
            scope.$watch(attrs.src, function(){
                if (hasLoaded) {
                    return;
                }
                var $img = $(element);
                var imgPreloader = new Image();

                imgPreloader.src = attrs.src;
                $img.attr('src', defaultImg);

                if (options.cls) {
                    $img.parent().addClass(options.cls);
                }

                var endLoading = function(isFail){
                    if (!isFail) {
                        $img.attr('src', imgPreloader.src);
                    }
                    hasLoaded = true;
                    if (options.cls) {
                        $img.parent().removeClass(options.cls);
                    }
                    if (options.transition) {
                        $img.transition({opacity: 1}, 150);
                    }
                    
                }

                if (imgPreloader.complete) {
                    endLoading();

                }
                else {
                    if (options.transition) {
                        $img.css({opacity: 0});
                    }
                    
                    imgPreloader.onload = function(){
                        endLoading();
                        hasLoaded = true;
                    }
                    imgPreloader.onerror = function(){
                        endLoading(true);
                    };
                }
            });
        }
    }
}]);

app.directive('pecacheHelper', [function(){
    return {
        link: function(scope, element, attrs){
            var preCacheArray = [
                '/static/images/blank.png'
            ];
            element.css('display', 'none');
            _.each(preCacheArray, function(imgSrc){
                element.append('<img src="'+imgSrc+'">');
            });
        }
    }
}]);

app.directive('autoresizeTextarea', [function(){
    return {
        link: function(scope, element, attrs){
            $(element).autoResize({
                maxHeight: 187,
                minHeight: 30,
                extraSpace: 16
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

app.directive('libLightbox', 
['$compile', '$templateCache', '$http', '$rootScope', 
function($compile, $templateCache, $http, $rootScope){
    return{
        restrict: 'A',
        template: '<div class=lightbox >'+
                      '<div class="lightboxBg" ng-click="close()" ng-class="{loading: loadingLightbox}">'+
                          '<div class="lightboxContent" stop-event="click" ng-show="!loadingLightbox"></div>'+
                          '</div>'+
                  '</div>',
        link: function(scope, element, attrs){
            // Life Cycle: appendLightbox -> directive(here) -> controller(lightboxFrameCtrl) -> ng-init in lightboxFrame.html

            element.addClass('lightboxWrap');
            var options = scope.$eval(attrs.libLightbox);
            $rootScope.lightboxMap = $rootScope.lightboxMap || {};
            scope.close = function(){
                scope.lightboxLevel = null;
                element.remove();
                $rootScope.lightboxMap[options.level] = null;
            };

            scope.closeAllLightbox = function(){
                angular.forEach($rootScope.lightboxMap, function(lightboxScope){
                    if(lightboxScope){
                        lightboxScope.close();
                    }
                });
            };

            scope.showLightboxContent = function(){
                scope.loadingLightbox = false;
            };

            if($rootScope.lightboxMap[options.level]){
                element.remove();
                return;
            }
            $rootScope.lightboxMap[options.level] = scope;
            scope.lightboxLevel = options.level;

            function showLightbox(html){
                element.find('.lightboxContent').append($compile(html)(scope));
                if(options.isDefer){
                    scope.loadingLightbox = true;
                }
                element.children().css('display', 'table');
            };
            
            if(!options.isTemplate){
                showLightbox(options.source);
            }else if(options.source){
                var cache = $templateCache.get(options.source);
                if(cache){
                    if(typeof(cache) == 'string'){
                        showLightbox(cache);
                    }else{
                        showLightbox(cache[1]);
                    }
                }else{
                    $http.get(options.source, {cache:$templateCache}).success(function(){
                        showLightbox($templateCache.get(options.source)[1]);
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


app.directive("lightboxImg", ['$rootScope', function($rootScope) {
    return {
        // require: "ngModel",
        scope: {
            lightboxImg: '='
        },
        link: function(scope, element, attrs, ctrl) {
            var newScope = scope.$new();
            newScope.lightboxImg = scope.lightboxImg;
            scope.showImgLightbox = function() {
                $rootScope.appendLightbox({
                    source: '/tpl/lightbox/imgDetail.html'
                }, newScope);
            }
        }
    };
}]);


app.directive('imgDetail', ['$timeout', '$window', function ($timeout, $window) {
    return{
        restrict: 'A',
        template: '<img ng-src="{[lightboxImg.original_raw]}" alt="" onerror="this.onerror=null;" id="imageContent" width={[imageWidth]} height={[imageHeight]}>',
        replace: true,
        link: function(scope, element, attrs){
            if (!scope.lightboxImg) {
                return;
            }

            var minWidth = 300;
            var minHeight = 180;
            var offsetHeight = 150;
            var offsetWidth = 150;
            var oWidth = scope.lightboxImg.original_width;
            var oHeight = scope.lightboxImg.original_height;
            
            function setSize(){
                var height = Math.max(Math.min($window.innerHeight-offsetHeight, oHeight), minHeight);
                var width = Math.round(height * oWidth / oHeight);
                if(width < minWidth){
                    width = minWidth;
                    height = width * oHeight / oWidth;
                }
                if(width > $window.innerWidth - offsetWidth){
                    width = $window.innerWidth - offsetWidth;
                    height = width * oHeight / oWidth;
                }
                $timeout(function(){
                    scope.lightboxFrameOptions.title = scope.lightboxImg.title;
                    scope.lightboxFrameOptions.style.width = width + 18;
                    scope.imageWidth = Math.min(width, oWidth);
                    scope.imageHeight = scope.imageWidth * oHeight / oWidth;
                    scope.showLightboxContent();
                });
                scope.showMagnify = (width < oWidth);
            }
            setSize();
            $($window).resize(setSize);
        }
    }
}]);


app.directive('scFileupload', [function () {
    return{
        restrict: 'A',
        link: function(scope, element, attrs){
            var uploaderEl = $('<input class="id_file" type="file" size="1" name="file" accept="'+attrs.accept+'">');

            var options = {
                url: attrs.url,
                type:"POST",
                dataType:'json',
                autoUpload: true,
                sequentialUploads: true,
                dropZone: null,
            };
            angular.extend(options, scope.$eval(attrs.scFileupload));
            
            uploaderEl.fileupload(options);
            element.append(uploaderEl);
            
        }
    }
}]);


app.directive('dragDropUpload', [function () {
    return{
        restrict: 'A',
        link: function(scope, element, attrs){
            // must set {uploadSelector:"#blah .cls"}
            var options = scope.$eval(attrs.dragDropUpload);
            var uploadSelector = options.uploadSelector;
            var makeRelative = options.makeRelative ? true: false;
            if (!uploadSelector) {
                console.log('should set uploadSelector');
                return;
            }

            function dragleave () {
                if (makeRelative) {
                    $(element).css({position:'static'});
                }
                $(element).find('.dragCover').remove();
            }

            $(element).bind('dragover', function(e){
                e.preventDefault();
                if ($(element).find('.dragCover').size()==0){
                    if (makeRelative) {
                        $(element).css({position:'relative'});
                    }
                    var dragCover = $('<div class="dragCover"></div>');
                    dragCover.on('dragleave', dragleave);
                    $(element).append(dragCover);
                    $(uploadSelector).fileupload('option', {
                        dropZone: dragCover
                    });
                }
            });
            $(element).bind('drop', function (e) {
                e.preventDefault();
                $(element).find('.dragCover').remove();
            });
        }
    }
}]);


app.directive('fitWindowHeight',['$window', function($window){
    return{
        restrict:'A',
        link: function(scope, element, attrs){
            var options = scope.$eval(attrs.fitWindowHeight);
            if(options.disable){
                return;
            }
            function seth(){
                var h = $window.innerHeight - (options.offset ? parseInt(options.offset, 10) : 0);
                var max = options.max ? parseInt(options.max, 10) : (h + 1);
                var min = options.min ? parseInt(options.min, 10) : (h - 1);
                element.height(_.max([_.min([h, max]), min]));
            };
            seth();
            $($window).resize(seth);
        }
    }
}]);


app.directive('openWindow', ['$window', '$timeout',function ($window, $timeout) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs){
            var options = {
                width: 500,
                height: 400,
                title: "window",
                url: '/',
                closeCallback: null
            };
            angular.extend(options, scope.$eval(attrs.openWindow));
            element.bind('click', function(){
                var win = $window.open(options.url, options.title, 'width='+options.width+',height='+options.height);
                if(angular.isFunction(options.closeCallback)){
                    var watchClose = setInterval(function() {
                        if (win.closed) {
                            clearTimeout(watchClose);
                            options.closeCallback();

                        }
                    }, 100);
                }    
            })
        }
    }
}]);


app.directive('scContextMenu', ['$timeout','utils',function ($timeout, utils) {
    return {
        restrict: 'A',
        link: function (scope, el, attr) {
            var options = {
                id: utils.genRandomKey(),
                callback: function(){},
                offsetX: 0,
                offsetY: 0
            };
            if (attr.contextMenuOptions) {
                var _options = scope.$eval(attr.contextMenuOptions);
                _.extend(options,  _options);
            }
            
            function open(){
                el.addClass('active');
                var tpl =   '<div class="contextMenu" id="'+options.id+'">'+
                                '<div class="contextMenuBg">'+
                                   
                                '</div>'+
                                '<ul class="contextMenuList">'+
                                '</ul>'+
                            '</div>';

                var menuEl = $(tpl);
                var items = scope[attr.scContextMenu];
                angular.forEach(items, function(val, key){
                    var cls = '';
                    if (val.length > 2) {
                        // Add class
                        cls = val[2];
                    }
                    var item = $('<li class="menuItem '+cls+'">'+val[0]+'</li>');
                    item.bind('click', function(e){
                        e.stopPropagation();
                        val[1](e, item);
                        close();
                    });
                    this.find('.contextMenuList').append(item);
                }, menuEl);
                menuEl.find('.contextMenuBg').bind('click', close);
                
                menuEl.appendTo(document.body);
                var listEl = menuEl.find('.contextMenuList')
                listEl.css({
                    top: el.offset().top + el.height() + options.offsetY + 5 + 'px',
                    left: el.offset().left - listEl.width() + el.width() + options.offsetX + 1 + 'px'
                });
                if(attr.menuZindex){
                    listEl.css({
                        'z-index': parseInt(attr.menuZindex, 10)
                    })
                }
            };

            function close(){
                el.removeClass('active');
                angular.element(document.getElementById(options.id)).remove();
                options.callback();
            };

            scope.$on('closeMenu', function(){
                close();
            });

            el.bind('click', function (e) {
                if(el.hasClass('active') ){
                    close();
                }else{
                    open();
                }
            });
        }
    };
}]);


