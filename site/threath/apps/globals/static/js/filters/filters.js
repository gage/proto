app.filter('newlines', [function() {
    return function(text) {
    	// Code review
        return text.replace(/\n/g, '<br/>');
    }
}]);


app.filter('escapeHtml', [function() {
    return function(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/>/g, '&gt;')
            .replace(/</g, '&lt;');
    }
}]);


app.filter('bytes', [function() {
    return function(bytes, precision) {
        if (isNaN(parseFloat(bytes)) || !isFinite(bytes)) return '-';
        if (typeof precision === 'undefined') precision = 1;
        var units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB'],
            number = Math.floor(Math.log(bytes) / Math.log(1024));
        return (bytes / Math.pow(1024, Math.floor(number))).toFixed(precision) +  ' ' + units[number];
    }
}]);


app.filter('parseLink', ['utils', function(utils) {
    return function(text) {
        var urls = utils.fetchUrls(text);
        // console.log(urls)
        if(urls && urls.length > 0){
            var tmp_urls = {};
            for(var i=0, len=urls.length; i<len; i++){
                var url = urls[i];
                var re_url = utils.escapeRegExp(url);
                if(tmp_urls[url])
                    continue;
                var re = RegExp(re_url, 'g');
                var href = (url.substring(0,7) != "http://" && url.substring(0,8) != "https://") ? 'http://'+url : url;
                text = text.replace(re, '<a href="'+href+'" target="_blank">'+url+'</a>');
                tmp_urls[url] = true;
            }
        }


        return text;
    }
}]);