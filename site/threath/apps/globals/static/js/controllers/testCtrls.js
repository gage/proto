app.controller('testUpload', ['$scope', '$compile', '$element', 'currentUser', function ($scope, $compile, $element, currentUser){
    $scope.uploadingImg = false;
    $scope.groupImg = '';
    $scope.photoId = null;
    $(function(){
        $($element.find('.id_file')).fileupload({
            url: '/api/photos/',
            type:"POST",
            dataType:'json',
            autoUpload: true,
            sequentialUploads: true,
            dropZone: null,
            add: function(e, data){
                $scope.uploadingImg = true;
                data.submit();
            },
            done: function (e, data) {
                $scope.uploadingImg = false;
                if(data.result.success){
                    var r = data.result.response;
                    $scope.photoId = r.id;
                    $scope.groupImg = r.prefix + 'i32' + r.extension;
                    // Add this line to force the image render
                    $scope.$apply();
                }else{
                    console.log("Failed to upload photo");
                }
            },
            fail: function(e, data){
                console.log('fail')
                $scope.uploadingImg = false;
            }
        });
    });

    
}])
