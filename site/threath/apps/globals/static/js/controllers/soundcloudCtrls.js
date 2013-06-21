app.controller('soundcloudCtrls.main',['$scope','$q', 'limitToFilter', '$http', 'utils', 'rSoundcloud', function($scope, $q, limitToFilter, $http, utils, rSoundcloud){
    $scope.sounds = rSoundcloud.initCollection();;
    $scope.query = '';
    $scope.loading = false;

    this.search = $.debounce(200, function(e, ui){
        if ($scope.loading) {
            return;
        }
        $scope.$apply();
        $scope.loading = true;
        var para = {
            q: $scope.query
        };

        if(ui && ui.item.value) {
            para.q = ui.item.value;
        }

        $scope.$apply(function(){
            var deferred = $scope.sounds.getData(para);
            deferred.then(function(sounds){
                $scope.sounds = sounds;
                $scope.loading = false;
            })
        })
        
    })

}]);


app.controller('soundcloudCtrls.item',['$scope','$q', 'utils', function($scope, $q, utils){
    $scope.openDetail = function(){
        utils.openDetailLightbox($scope, {
           apiPrefix: '/api/soundcloud/',
           iframeUrl: '/static/device_webview/html/sc_music_info_tpl.html',
           iframeObj: $scope.sound,
           lightboxHeight: 580
       })
    }
}]);


