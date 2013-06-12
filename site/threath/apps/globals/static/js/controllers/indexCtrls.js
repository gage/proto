app.controller('indexCtrls.main',['$scope','$window', function($scope, $window){
    
    $scope.testMenuInit = {
        test1: ['Test one', function(){
            alert('test 1');
        }, 'cls1'],
        test2: ['Test two', function(){
            alert('test 2');
        }, 'cls2']
    };
}]);

app.controller('indexCtrls.tagWidget',['$scope','$window', 'limitToFilter', '$http', function($scope, $window, limitToFilter, $http){
    $scope.states = function(cityName) {
        return $http.jsonp("http://gd.geobytes.com/AutoCompleteCity?callback=JSON_CALLBACK &filter=US&q="+cityName).then(function(response){
            return limitToFilter(response.data, 15);
        });
    };

    $scope.onAddTag = function(e){
        alert($scope.selected);

    };

    $scope.select2Options = {
        data: [{id: 'redbean', text: 'redbean'}],
        tags: true,
        tokenSeparators: [",", " "],
        createSearchChoice: function(term, data) {
            if ($(data).filter(function() {
                return this.text.localeCompare(term) === 0;
            }).length === 0) {
                return {
                    id: term,
                    text: term
                };
            }
        },
        multiple: true,
        ajax: {
            url: "/api/tag/",
            dataType: "json",
            data: function(term, page) {
                return {
                    q: term
                };
            },
            results: function(data, page) {
                var rtn = [];

                // Fake object
                _.each(data.response, function(tagTxt){
                    var rtnObj = {id: tagTxt, text: tagTxt};
                    rtn.push(rtnObj);
                });
                return {
                    results: rtn
                };
            }
        }
    };

}]);


app.controller('indexCtrls.youtubeWidget',['$scope','$window', 'limitToFilter', '$http', 'utils', function($scope, $window, limitToFilter, $http, utils){

    $scope.onAddTag = function(e){
        // alert($scope.selected);

    };

    this.selectCallback = function(e){
        
        var object = e.added;
        var youtubeId = object.id;
        var title = object.title;
        utils.openYoutubeLightbox(youtubeId, title);
    }

    $scope.select2Options = {
        data: [],
        tokenSeparators: [",", " "],
        multiple: true,
        escapeMarkup: function (m) { return m; },
        // closeOnSelect: false,
        formatResult: function(youtube) {
            var wrapper = $('<div></div>');
            wrapper.attr('class', 'youtubeWrap');
            wrapper.append('<img src="'+youtube.thumburl+'"><div class="title">'+youtube.title+'</div><div>Views: '+youtube.view_count+'</div>');
            return wrapper;
        },
        dropdownCssClass: "searchDrop",
        ajax: {
            url: "/api/youtube/",
            dataType: "json",
            data: function(term, page) {
                return {
                    q: term
                };
            },
            results: function(data, page) {
                var rtn = [];

                // Fake object
                _.each(data.response, function(obj){
                    var rtnObj = {id: obj.youtube_id, text: obj.title, thumburl: obj.thumburl, title: obj.title, view_count:obj.view_count};
                    rtn.push(rtnObj);
                });
                return {
                    results: rtn
                };
            }
        }
    };

}]);

app.controller('indexCtrls.googleWidget',['$scope','$window', 'limitToFilter', '$http', 'utils', function($scope, $window, limitToFilter, $http, utils){
    // http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%E4%BA%94%E6%9C%88%E5%A4%A9&rsz=8

    this.selectCallback = function(e){}

    $scope.select2Options = {
        data: [],
        tokenSeparators: [",", " "],
        multiple: true,
        escapeMarkup: function (m) { return m; },
        formatResult: function(google) {
            var wrapper = $('<div></div>');
            wrapper.attr('class', 'googleWrap');
            wrapper.append('<div class="title">'+google.title+'</div><div>Content:'+google.content+'</div>');
            return wrapper;
        },
        dropdownCssClass: "searchDrop",
        ajax: {
            url: "http://ajax.googleapis.com/ajax/services/search/web",
            dataType: "jsonp",
            data: function(term, page) {
                return {
                    'v': '1.0',
                    'q': term,
                    'rsz': 8,
                    'start': 0
                };
            },
            results: function(data, page) {
                var rtn = [];
                var processed = data.responseData.results;
                // Fake object
                _.each(processed, function(obj){
                    var rtnObj = {id: obj.url, text: obj.title, title: obj.title, content:obj.content};
                    rtn.push(rtnObj);
                });
                return {
                    results: rtn
                };
            }
        }
    };

}]);


app.controller('indexCtrls.googleImageWidget',['$scope','$q', 'limitToFilter', '$http', 'utils', function($scope, $q, limitToFilter, $http, utils){
    // http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=japan&rsz=8

    this.selectCallback = function(e){}
    $scope.images = [];
    $scope.query = '';
    $scope.loading = false;

    this.search = $.debounce(200, function(e, ui){
        if ($scope.loading) {
            return;
        }
        $scope.$apply();
        $scope.loading = true;
        var para = {
            v: '1.0',
            q: $scope.query,
            rsz: 8
        };

        if(ui && ui.item.value) {
            para.q = ui.item.value;
        }

        $scope.$apply(function(){
            $http.jsonp('http://ajax.googleapis.com/ajax/services/search/images?callback=JSON_CALLBACK&'+utils.serialize(para)).then(function(r){
                var data = r.data;
                $scope.images = data.responseData.results;
                para.start = 8
                $http.jsonp('http://ajax.googleapis.com/ajax/services/search/images?callback=JSON_CALLBACK&'+utils.serialize(para)).then(function(r){
                    var data = r.data;
                    $scope.images = $scope.images.concat(data.responseData.results)
                    $scope.loading = false;
                });
            });
        })
        
    })

}]);



app.controller('indexCtrls.photoWidget',['$scope','$window', 'remotePhoto', function($scope, $window, remotePhoto){
    $scope.loading = false;
    $scope.photos = remotePhoto.initCollection();
    var remotePhotoPromise = remotePhoto.query().then(function(resolved){
        $scope.photos = resolved;
        $scope.loading = false;

    }, function(errmsg){
        $scope.loading = false;
    });

    $scope.uploadOption = {};

    $scope.onFileUploadAdd = function(e, data){
        var limit = 80000000;
        if(data.files[0].type.match(/^image\/(gif|jpeg|png|jpe)$/)){
            data.url = '/api/photos/';
            // limit = 3000000;
        }
        else{
            console.log('not support');
            return;
        }
        // TODO: video
        if(data.files[0].size > limit){
            alert('The Limit of File Size is 80MB');
            return;
        }

        var uploadingMsgObj = {
            filename: data.files[0].name
        };
        // Code Review

        data.submit();
    };

    $scope.onFileUploadProgress = function(e, data){
        $scope.uploadingPercent = parseInt(data.loaded / data.total * 100, 10);
        if(!$scope.$root.$$phase) {
            $scope.$apply();
        }
    };

    $scope.onFileUploadDone = function(e, data){
        console.log('complete');
    };

    $scope.onFileUploadFail = function(e, data){
    };

}]);

app.controller('indexCtrls.photoItem',['$scope','$window', function($scope, $window, remotePhoto){

}]);






// =============== Testing code ==================

app.controller('indexCtrls.testAutoGrowth', ['$scope', '$compile', '$element', 'currentUser', 'remotePhoto', function ($scope, $compile, $element, currentUser, remotePhoto){

}]);

app.controller('indexCtrls.testRemote', ['$scope', '$compile', '$element', 'currentUser', 'remotePhoto', function ($scope, $compile, $element, currentUser, remotePhoto){
    $scope.loading = false;
    $scope.remotePhotos = remotePhoto.initCollection();
    var remotePhotoPromise = remotePhoto.query().then(function(resolved){
        $scope.remotePhotos = resolved;
        $scope.loading = false;

    }, function(errmsg){
        $scope.loading = false;
    });
}]);
