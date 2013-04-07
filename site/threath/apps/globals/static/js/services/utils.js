app.service('utils', [ function(){
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


    return utils;
}]);