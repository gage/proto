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

app.controller('indexCtrls.photoWidget',['$scope','$window', function($scope, $window, remotePhoto){
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
