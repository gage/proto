
angular.module('remoteData', [])
.factory('$remoteData', ['$http', '$q', function($http, $q){
    
    function remoteDataFactory(params){
        function dataObj(value, collection){
            angular.copy(value || {}, this);
            this.getCollection = function(){
                return collection;
            }
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

        function format(list, collection){
            for(var i=0,len=list.length;i<len;i++){
                list[i] = new dataObj(list[i], collection);
            };
            return list;
        };
        

        dataObj.initCollection = function(collectionOptions){
            // Fallback comparator
            return new dataCollection(collectionOptions);
        };

        dataObj.query = function(data, collectionOptions){
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
                var collectionObj = {
                    models: parse(data),
                    raw: data,
                    comparator: params.comparator
                }
                if(angular.isObject(collectionOptions)){
                    angular.extend(collectionObj, collectionOptions);    
                }
                var collection = new dataCollection(collectionObj);
                collection.sort();
                deferred.resolve(collection);
            })
            .error(function(data, status, headers, config){
                var errmsg = '';
                deferred.reject(errmsg);
            });

            return deferred.promise;
        };

        dataObj.getCollectionClass = function(){
            return dataCollection;
        }

        dataObj.getCollection = function(){
            // The collection will be added at wrap function e.g. "format"
            return null;
        }

        dataObj.prototype.save = function(){
            alert('save: not implemented')
        }

        dataObj.prototype.set = function(data){
            angular.extend(this, data);
        };

        // Data collection

        function dataCollection(value){
            angular.copy(value || {}, this);
            // Wrap it with dataObj
            this.models = format(this.models || [], this);
            // Attributes:
            // comparator
            if (value==null || value.comparator==null) {
                this.comparator = params.comparator;
            }

        };


        // An alternate way to fetch data.
        dataCollection.prototype.fetch = function(data){
            var _this = this;
            var deferred = $q.defer();
            if (!this.url) {
                this.url = url;
            }
            var queryUrl = typeof this.url=='function'? this.url():this.url;
            if(data){
                var str = [];
                for(var p in data)
                    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(data[p]));
                var dataStr = str.join("&");
                queryUrl = queryUrl + '?' + dataStr;
            }
            $http.get(queryUrl)
                .success(function(data, status, headers, config){
                    // Collection === this
                    var collection = _this.init({
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

        dataCollection.prototype.inPlaceFilter = function(func){
            var filtered = _.filter(this.models, func);
            this.models.length = 0;
            for (var i=0,len=filtered.length;i<len;i++) {
                this.models[i] = filtered[i];
            }
        }

        var fnList = ['each', 'first', 'last', 'find', 'uniq','filter', 'contains'];
        // can add but need verify (add them when needed)
        // ['map']

        // Hook underscore functions
        _.each(fnList, function(fnName){
            dataCollection.prototype[fnName] = function(args) {
                // Apply arguments
                return _[fnName].apply(this, [this.models].concat(Array.prototype.slice.call(arguments)));
            }
        });

        dataCollection.prototype.init = function(value) {
            // Reset the models but not lose the reference
            this.models.length = 0;
            var newModels = [];
            if (value && value.models) {
                newModels = value.models;
                delete value.models;
            }
            _.extend(this, value || {});
            // Wrap it with dataObj
            if (newModels) {
                this.add(newModels);
            }
            return this;
        }

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

            var wrapObjs = format(objs, this);
            var objIds = _.pluck(wrapObjs, 'id');
            _.each(wrapObjs, function(wrapObj){
                var existObj = _this.find(function(obj){return obj.id==wrapObj.id;});
                if (!existObj) {
                    _this.models.push(wrapObj);
                }
                else {
                    // Set attributes of new object into existing object
                    existObj.set(wrapObj);
                }
            });
            this.sort();
            // Find the added objects to return
            var addedModels = this.filter(function(obj){return _.contains(objIds, obj.id);});
            return isAddModel ? wrapObjs[0]:wrapObjs;
        }

        dataCollection.prototype.length= function() {
            return this.models.length;
        }

        dataCollection.prototype.get = function(id){
            var target = false;
            for(var i=0, len=this.models.length;i<len; i++){
                if(this.models[i].id == id){
                    target = this.models[i];
                }
            }
            return target;
        }

        dataCollection.prototype.remove = function(id){
            var target = false;
            for(var i=0, len=this.models.length;i<len; i++){
                if(this.models[i].id == id){
                    this.models.splice(i,1);
                    target = true;
                    break;
                }
            }
            return target;
        }

        // Attach collection for each remoteData usage
        // e.g. friendList.collection.prototype.loadMore = function() {};
        dataObj.collection = dataCollection;

        return dataObj;
    }

    return remoteDataFactory;
}]);


















