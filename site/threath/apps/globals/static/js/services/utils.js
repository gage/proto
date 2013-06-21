app.service('utils', ['$rootScope', '$q', '$http', function($rootScope, $q, $http){
    var utils = {};
    


    String.prototype.sequenceMatch = function(str, isCaseSensitive) {
        var p_str = "";
        for(var j=0; j<str.length; j++){
            if(j+1 != str.length)
                p_str += str[j] + ".*";
            else
                p_str += str[j]
        }
        if(isCaseSensitive)
            var p = new RegExp(p_str);
        else
            var p = new RegExp(p_str,'i');
        if(this.search(p) == -1)
            return false
        else
            return true
    }
    String.prototype.startsWith = function(str) {
        return (this.match("^"+str)==str)
    }

    String.prototype.endsWith = function(str) {
        return (this.match(str+"$")==str)
    }

    utils.validateEmail = function(email){
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    };

    utils.genRandomKey = function(len){
        if(!len || len < 5){
            len = 5;
        };
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        for( var i=0; i < len; i++ ){
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        }
        return text;
    };

    utils.fetchUrls = function(content){
        content = utils.htmlDecode(content);
        var groups = content.match( /(?:https?:\/\/)?@?(?:(?:[\w-]+)\.){1,4}(?:(aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|xxx|im|[a-z]{2})\b)(\.[a-zA-Z]{2})?(?:[:\/\?#$]{1}[\w\.,&#=\-+%!\(\)~]*)*/g );

        if (groups){
            var filtered_groups = groups.filter(function(x){ return _.first(x) != "@"});
            if (filtered_groups.length){
                return filtered_groups;                    
            }
        }
        return null;
    };

    utils.openInNewTab = function(url){
        var win=window.open(url, '_blank');
        win.focus();
    };

    utils.escapeRegExp = function(str){
        return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
    };


    utils.confirm = function(args, scope){
        // Need Confirm
        var options = {
            title: 'Confirm',
            message: 'Do you want to do this?',
            level: 1,
            source:'/tpl/lightbox/confirmDialog.html',
            width: 300
        };
        _.extend(options, args);
        options.level = scope && scope.lightboxoptions ? scope.lightboxoptions.level+1: 1;
        options.deferred = $q.defer();
        options.parentScope = scope;

        $rootScope.appendLightbox(options);
        return options.deferred.promise;
    }

    utils.getQueryVariable = function(url, variable) {
        var query = url.split('?')[1];
        if (!query) {
            return '';
        }
        var vars = query.split('&');
        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split('=');
            if (decodeURIComponent(pair[0]) == variable) {
                return decodeURIComponent(pair[1]);
            }
        }
    };

    utils.serialize = function(obj) {
        var str = [];
        for(var p in obj)
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        return str.join("&");
    }

    utils.openYoutubeLightbox = function(youtubeId, title, rawUrl, scope){
        var newScope = $rootScope.$new();
        if (!scope) {
            scope = newScope;
        }
        
        var $container = $('<div><div id="youtubeVideo"><div class="info-content"></div></div></div>');
        var startTime = '';
        // Parse start time
        if (rawUrl) {
            var startTimeValue = utils.getQueryVariable(rawUrl, 't');
            if (startTimeValue) {
                startTime = '#t='+startTimeValue;
            }
        }
        var youtubeSrc = 'http://www.youtube.com/embed/'+youtubeId+'?rel=0&hd=1&vq=hd1080&autoplay=1'+startTime;
        newScope.youtubeSrc = youtubeSrc;
        $rootScope.appendLightbox({
            source: '/tpl/lightbox/youtube.html',
            level: scope.lightboxLevel + 1
        }, newScope);
    }


    utils.openDetailLightbox = function(scope, options){
        // defaults show the specs of options
        var defaults = {
            apiPrefix: '',
            iframeUrl: '',
            iframeObj: null
        };

        var newScope = $rootScope.$new();
        _.extend(newScope, options);

        $rootScope.appendLightbox({
            source: '/tpl/lightbox/detail.html',
            level: scope.lightboxLevel + 1,
            isDefer: true
        }, newScope);
    }



    return utils;
}]);