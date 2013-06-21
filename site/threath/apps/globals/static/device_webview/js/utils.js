// This is a util js file for device

var DeUtils = (function (_DeUtils) {

    // _DeUtils.debug = true;

    // Initialize
    _DeUtils.defaults = {
        imageSpec: 'i256'
    };

    _DeUtils.initFastClick = function(FastClick) {
        window.addEventListener('load', function() {
            new FastClick(document.body);
        }, false);
    };

    // Prototype
    _DeUtils.renderObj = function(jsonStr, options) {
        // jsonStr = jsonStr;
        var obj = _DeUtils.initRenderInfo(jsonStr, options);
        return jsonStr;
    };

    _DeUtils.initRenderInfo = function(jsonStr, options) {
        var obj;
        if (typeof(jsonStr)=='string') {
            obj = JSON.parse(jsonStr);
        }
        else {
            obj = jsonStr;
        }

        var infoWrapper = document.querySelector('.info-wrapper');
        if (options && options.device=='desktop') {
            
            _DeUtils.addClass(infoWrapper, 'desktop');
            _DeUtils.defaults.imageSpec = 'i128';

            // Share
            if (document.querySelector('.info-wrapper .shareBtn')) {
                document.querySelector('.info-wrapper .shareBtn').onclick = function(e) {
                    _DeUtils.onClickShare(e);
                }
            }
        }

        if (options && options.displayAs=='attach') {
            _DeUtils.addClass(infoWrapper, 'attach');
        }

        return obj;
    };

    _DeUtils.initRenderCard = function(jsonStr, options) {
        var obj;

        document.body.addEventListener("click", function(){
            NativeBridge.call("viewDetail",{});
        }, false);

        if (typeof(jsonStr)=='string') {
            obj = JSON.parse(jsonStr);
        }
        else {
            obj = jsonStr;
        }

        if (options && options.device=='desktop') {
            var cardWrapper = document.querySelector('.card-wrapper');
            _DeUtils.addClass(cardWrapper, 'desktop');
            _DeUtils.defaults.imageSpec = 'i128';
        }

        return obj;
    };

    _DeUtils.onClickCover = function(e) {
    };

    _DeUtils.onClickShare = function(e) {
    };

    // Utils

    _DeUtils.formatDuration = function(duration){
        var m = parseInt(duration/60,10);
        var s = parseInt(duration - m*60,10);
        return ((m<10)?'0'+m:m) + ':' + ((s<10)?'0'+s:s);
    };

    _DeUtils.getMovieTime = function(runtime) {
        var runtimeMin = runtime % 60;
        var runtimeHour = Math.floor(runtime / 60);
        var rtnStr = '';
        if (runtimeHour!=0) {
            rtnStr = runtimeHour + ' hr. ';
        }
        rtnStr += (runtimeMin + ' min.');
        return rtnStr;
    };

    _DeUtils.getShowTime = function(showtime) {
        var cleanedShowtime = new Array();
        var idx = showtime.length - 1;
        var state = '';
        for (; idx >=0 ; idx--) {
            var displayTime = showtime[idx];
            if (displayTime.endsWith('pm')) {
                state = 'pm';
                displayTime = displayTime.slice(0, displayTime.length-2);
            }
            if (displayTime.endsWith('am')) {
                state = 'am';
                displayTime = displayTime.slice(0, displayTime.length-2);
            }
            if (state=='pm') {
                var hour = displayTime.split(':')[0];
                var min = displayTime.split(':')[1];
                if (hour!=12) {
                    hour = parseInt(hour) + 12;    
                }
                displayTime = ''+hour+':'+min;
            }
            cleanedShowtime.push(displayTime);
        }
        cleanedShowtime.reverse();
        return cleanedShowtime;
    };

    _DeUtils.readableFileSize = function(size) {
        var units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        var i = 0;
        while(size >= 1024) {
            size /= 1024;
            ++i;
        }
        return size.toFixed(1) + ' ' + units[i];
    };

    _DeUtils.shortenFileName = function(filename, max) {
        max = max ? max: 185;
        var rtn = filename;
        if (filename.visualLength() > max) {
            var ext = filename.split('.').slice(-1)[0];
            var tailSize = ext.length + 3;
            var tail = filename.slice(-tailSize);
            var tailLen = tail.visualLength();
            rtn = filename.trimToPx(max-tailLen) + tail;
        }
        return rtn;
    };


    _DeUtils.styleWidget = function(domId) {
        var opRow = document.getElementById(domId);
        opRow.addEventListener("touchstart", function(e){
            var opRow = document.getElementById(domId);
            _DeUtils.addClass(opRow, 'active');
        }, true);
        opRow.addEventListener("touchend", function(e){
            var opRow = document.getElementById(domId);
            _DeUtils.removeClass(opRow, 'active');
        }, true);
    }

    // _DeUtils.shortenFileName = function(filename, max) {
    //     max = max ? max: 20;
    //     var rtn = filename;
    //     if (filename.length > max) {
    //         var ext = filename.split('.').slice(-1)[0];
    //         var tailSize = ext.length + 3;
    //         var tail = filename.slice(-tailSize);
    //         rtn = filename.slice(0, max-tailSize) + '...' + tail;
    //     }
    //     return rtn;
    // };

    _DeUtils.hideDomById = function (domId) {
        var dom = document.getElementById(domId);
        _DeUtils.addClass(dom, 'hide');
    };

    _DeUtils.showDomById = function (domId) {
        var dom = document.getElementById(domId);
        _DeUtils.removeClass(dom, 'hide');
    };

    _DeUtils.hideDom = function (dom) {
        _DeUtils.addClass(dom, 'hide');
    };

    _DeUtils.removeDom = function (dom) {
        dom.parentNode.removeChild(dom);
    };

    _DeUtils.getPhotoUrl = function (photoObj,spec) {
        return photoObj.prefix + spec + photoObj.extension;
    };

    _DeUtils.include = function (arr,obj) {
        return (arr.indexOf(obj) !== -1);
    };

    _DeUtils.setBackground = function(dom, url) {
        dom.style.backgroundImage = 'url('+url+')';
    };

    _DeUtils.setBackgroundColor = function(dom, color) {
        dom.style.backgroundColor = color;
    };

    _DeUtils.covertTimestamp = function (ts) {
        var d = new Date(ts*1000);
        var date = d.getDate();
        var month = d.getMonth()+1;
        var year = d.getYear()+1900;
        return date+"/"+month+"/"+year;
    };

    _DeUtils.hasClass = function(dom, className) {
        var regExp = new RegExp('(\\s|^)'+className+'(\\s|$)');
        return regExp.test(dom.className);
    };

    _DeUtils.addClass = function(dom, className) {
        if (!_DeUtils.hasClass(dom, className)) {
            dom.className += ' '+className;
        }
    };
    _DeUtils.removeClass = function(dom, className) {
        dom.className = dom.className.replace(new RegExp('(?:^|\\s)'+className+'(?!\\S)') , '');
    };

    // Render or Create Dom
    _DeUtils.renderMap = function(location, mapContainerId) {
        var locationStr = location.join(',');
        var mapContainer = document.getElementById(mapContainerId);
        var img = document.createElement('img');
        var mapUrl = 'http://maps.googleapis.com/maps/api/staticmap?center='+locationStr+'&zoom=15&size=539x303&sensor=false&scale=2&markers=color:red%7C'+locationStr;
        img.src = mapUrl;
        mapContainer.appendChild(img);
    };

   _DeUtils.openGoogleMap = function(lat, lng) {
       var url = 'https://maps.google.com.tw/maps?q='+lat+','+lng;
       var win = window.open(url, '_blank');
       win.focus();
   }; 

    _DeUtils.renderCardCover = function(scope, photo, spec) {
        // Photo could be 'string' or 'gulu photo object'
        var coverImg = document.querySelector(scope+'coverImg');
        var imgUrl = photo;
        if (spec==null) {
            spec = _DeUtils.defaults.imageSpec;
        }
        if (typeof(photo)==='object') {
            imgUrl = _DeUtils.getPhotoUrl(photo, spec);
        }
        _DeUtils.setBackground(coverImg, imgUrl);
    };

    _DeUtils.wrapPhone = function(phone){
        var content = phone;
        return content;
    }

    _DeUtils.renderCategories = function(category) {
        // Category is a list: User for movie card & info
        var displayTxt = '';
        if (category.length) {
            var categoryTxt = category.join(', ');
            displayTxt = 'Categories: ' + categoryTxt;
        }
        return displayTxt;
    };

    _DeUtils.createCallDom = function(phone) {
        // Create a button that can be pressed by mobile user
        var content = '<a href="tel:'+phone+'" style="color:#666;"><div class="label">Call</div><span class="content phone">'+phone+'</span></a>';
        var dom = document.createElement('div');
        dom.className = "call-wrapper op-button";
        dom.innerHTML = content;
        dom.addEventListener('click', function(e){
            e.stopPropagation();
        });
        return dom;
    };

    _DeUtils.createEmailDom = function(email) {
        // Create a button that can be pressed by mobile user
        var content = '<div class="label">E-mail</div><span class="content email">'+email+'</span>';
        var dom = document.createElement('div');
        dom.className = "email-wrapper op-button";
        dom.innerHTML = content;
        dom.addEventListener('click', function(e){
            NativeBridge.call("sendEmail", {email:email});
            e.stopPropagation();
        });
        return dom;
    };

    _DeUtils.createmMapDom = function(distance) {
        // Create a button that can be pressed by mobile user
        var content = '<div class="label">Map</div><span class="content map">'+distance+'</span>';
        var dom = document.createElement('div');
        dom.className = "map-wrapper op-button";
        dom.innerHTML = content;
        return dom;
    };

    _DeUtils.createShareDom = function() {
        var content = '<div class="share wrap"><div class="info-wrap"><div class="icon"></div><div class="label">Share</div></div></div> <div class="collect wrap"><div class="info-wrap"><div class="icon"></div><div class="label">Collect Card</div></div></div>';
        var dom = document.createElement('div');
        dom.className = "share-btns-wrap";
        dom.innerHTML = content;
        return dom;
    };

    return _DeUtils;
}(DeUtils || {}));


// Extend prototype
String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

String.prototype.visualLength = function() {
    var ruler = document.getElementById('ruler');
    ruler.innerHTML = this;
    return ruler.offsetWidth;
}

String.prototype.trimToPx = function(length) {
    var tmp = this;
    var trimmed = this;
    if (tmp.visualLength() > length)
    {
        trimmed += "...";
        while (trimmed.visualLength() > length)
        {
            tmp = tmp.substring(0, tmp.length-1);
            trimmed = tmp + "...";
        }
    }
    
    return trimmed;
}


// Libraries

/* ***** BEGIN LICENSE BLOCK *****
# Copyright 2010 Alexandre Poirot
#
# Contributor(s):
#   Alexandre poirot <poirot.alex@gmail.com>
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.
#
# ***** END LICENSE BLOCK *****/


var NativeBridge = {
  callbacksCount : 1,
  callbacks : {},

  // Automatically called by native layer when a result is available
  resultForCallback : function resultForCallback(callbackId, resultArray) {
    try {
    var callback = NativeBridge.callbacks[callbackId];
    if (!callback) {return;}

    callback.apply(null,resultArray);
    } catch(e) {
        // alert(e)
    }
  },

  // Use this in javascript to request native objective-c code
  // functionName : string (I think the name is explicit :p)
  // args : array of arguments
  // callback : function with n-arguments that is going to be called when the native code returned
  call : function call(functionName, args, callback) {

    var hasCallback = callback && typeof callback === "function";
    var callbackId = hasCallback ? NativeBridge.callbacksCount++ : 0;

    if (hasCallback) {
        NativeBridge.callbacks[callbackId] = callback;
    }

    var iframe = document.createElement("IFRAME");
    iframe.setAttribute("src", "js-frame:" + functionName + ":" + callbackId+ ":" + encodeURIComponent(JSON.stringify(args)));
    document.documentElement.appendChild(iframe);
    iframe.parentNode.removeChild(iframe);
    iframe = null;


  }

};


preventDefault = function(e){
    e.preventDefault();
}
