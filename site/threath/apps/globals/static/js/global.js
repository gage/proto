// rewrite $.ajax to support AjaxQueue and Abort mode
(function($) {

    var ajax = $.ajax,
        pendingRequests = {},
        synced = [],
        syncedData = [],
        ajaxRunning = [];

    $.ajax = function(settings) {
        // create settings for compatibility with ajaxSetup
        settings = jQuery.extend(settings, jQuery.extend({}, jQuery.ajaxSettings, settings));

        var port = settings.port;

        switch (settings.mode) {
            case "abort":
                if (pendingRequests[port]) {
                    pendingRequests[port].abort();
                }
                return pendingRequests[port] = ajax.apply(this, arguments);
            case "queue":
                var _old = settings.complete;
                settings.complete = function() {
                    if (_old) {
                        _old.apply(this, arguments);
                    }
                    if (jQuery([ajax]).queue("ajax" + port).length > 0) {
                        jQuery([ajax]).dequeue("ajax" + port);
                    } else {
                        ajaxRunning[port] = false;
                    }
                };

                jQuery([ajax]).queue("ajax" + port, function() {
                    ajax(settings);
                });

                if (jQuery([ajax]).queue("ajax" + port).length == 1 && !ajaxRunning[port]) {
                    ajaxRunning[port] = true;
                    jQuery([ajax]).dequeue("ajax" + port);
                }

                return;
            case "sync":
                var pos = synced.length;

                synced[pos] = {
                    error: settings.error,
                    success: settings.success,
                    complete: settings.complete,
                    done: false
                };

                syncedData[pos] = {
                    error: [],
                    success: [],
                    complete: []
                };

                settings.error = function() { syncedData[pos].error = arguments; };
                settings.success = function() { syncedData[pos].success = arguments; };
                settings.complete = function() {
                    syncedData[pos].complete = arguments;
                    synced[pos].done = true;

                    if (pos == 0 || !synced[pos - 1])
                        for (var i = pos; i < synced.length && synced[i].done; i++) {
                        if (synced[i].error) synced[i].error.apply(jQuery, syncedData[i].error);
                        if (synced[i].success) synced[i].success.apply(jQuery, syncedData[i].success);
                        if (synced[i].complete) synced[i].complete.apply(jQuery, syncedData[i].complete);

                        synced[i] = null;
                        syncedData[i] = null;
                    }
                };
        }
        return ajax.apply(this, arguments);
    };
    
})(jQuery);

if(typeof console == 'undefined'){
    console = {};
    console.log = function(){};
    console.debug = function(){};
    console.warn = function(){};
    console.error = function(){};
    console.info = function(){};
}

// String extended functions
String.prototype.endsWith = function(str) {
    return (this.match(str+"$")==str)
}

String.prototype.startsWith = function(str) {
    return (this.match("^"+str)==str)
}

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

String.prototype.Blength = function() {
    var arr = this.match(/[^\x00-\xff]/ig);
    return  arr == null ? this.length : this.length + arr.length;
}

if(typeof String.prototype.trim !== 'function') {
    String.prototype.trim = function() {
      return this.replace(/^\s+|\s+$/g, '');
    }
}


// form serialize object
$.fn.serializeObject = function(){
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};


// Array indexOf for <IE7
if (!Array.prototype.indexOf){
  Array.prototype.indexOf = function(elt /*, from*/)
  {
    var len = this.length >>> 0;

    var from = Number(arguments[1]) || 0;
    from = (from < 0)
         ? Math.ceil(from)
         : Math.floor(from);
    if (from < 0)
      from += len;

    for (; from < len; from++)
    {
      if (from in this &&
          this[from] === elt)
        return from;
    }
    return -1;
  };
}




var Site = Site || {};
Site.Views = Site.Views || {};
Site.Models = Site.Models || {};
Site.Collections = Site.Collections || {};