
angular.module('remoteData', [])
.factory('$remoteData', ['$http', '$q', function($http, $q){
    
    function remoteDataFactory(params){
        function dataObj(value){
            angular.copy(value || {}, this);
        };

        var url = '';
        if(typeof params.url == "function"){
            url = params.url();
        }else if(typeof params.url == "string"){
            url = params.url;
        };

        function parse(data){
            if(typeof params.parse =="function"){
                data = params.parse(data);
            }
            return data;
        };

        function format(list){
            for(var i=0,len=list.length;i<len;i++){
                list[i] = new dataObj(list[i]);
            };
            return list;
        };
        

        dataObj.initCollection = function(){
            // Return a dummy dataCollection for init usage
            return new dataCollection();
        };

        dataObj.query = function(data){
            var deferred = $q.defer();
            var queryUrl = url;
            if(data){
                var keys = _.keys(data);
                var dataStr = '';
                for(var i=0,len=keys.length;i<len;i++){
                    dataStr = dataStr + keys[i] + '=' + data[keys[i]] + '&';
                }
                queryUrl = queryUrl + '?' + dataStr;
            }
            $http.get(queryUrl)
                .success(function(data, status, headers, config){
                    var collection = new dataCollection({
                            models: parse(data),
                            raw: data,
                            comparator: params.comparator
                        });
                    collection.sort();
                    deferred.resolve(collection);
                })
                .error(function(data, status, headers, config){
                    var errmsg = '';
                    deferred.reject(errmsg);
                });
            return deferred.promise;
        };

        dataObj.prototype.save = function(){
            alert('save: not implemented')
        }

        // Data collection

        function dataCollection(value){
            angular.copy(value || {}, this);
            // Wrap it with dataObj
            this.models = format(this.models || []);
            // Attributes:
            // comparator
        };

        var fnList = ['each', 'first', 'last', 'find', 'uniq', 'filter']
        // can add but need verify (add them when needed)
        // ['map']

        // Hook underscore functions
        _.each(fnList, function(fnName){
            dataCollection.prototype[fnName] = function(args) {
                // Apply arguments
                return _[fnName].apply(this, [this.models].concat(Array.prototype.slice.call(arguments)));
            }
        });

        dataCollection.prototype.sort = function() {
            var copies = _.sortBy(this.models, this.getComparator());
            for (var i=0,len=this.length();i<len;i++) {
                this.models[i] = copies[i];
            }
        }

        dataCollection.prototype.getComparator = function() {
            return typeof this.comparator=="function" ? this.comparator : 0;
        }

        dataCollection.prototype.add = function(objs) {
            var _this = this;
            var isAddModel = false;
            if(Object.prototype.toString.call(objs) !== '[object Array]'){
                // Model
                isAddModel = true;
                objs = [objs];
            }

            var wrapObjs = format(objs);
            var objIds = _.pluck(wrapObjs, 'id');
            _.each(wrapObjs, function(wrapObj){
                if (!_this.find(function(obj){return obj.id==wrapObj.id;})) {
                    _this.models.push(wrapObj);
                }
            });
            this.sort();
            // Find the added objects to return
            var addedModels = this.filter(function(obj){return _.contains(objIds, obj.id);});
            return isAddModel ? addedModels[0]:addedModels;
        }

        dataCollection.prototype.length= function() {
            return this.models.length;
        }

        return dataObj;
    }

    return remoteDataFactory;
}]);


















