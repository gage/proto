app.controller('geoCtrls.main',['$scope','$window', function($scope, $window){
    $scope.geoInfo = {
        places: [],
        data: null,
        loading: false,
        instImages: [],
        fsPhotos: []
    }; 
    $scope.getLatlon = function(){
        var geoInfo = $scope.geoInfo;
        if (geoInfo.data) {
            return [geoInfo.data.geometry.location.lat, geoInfo.data.geometry.location.lng];
        }
        else {
            return [];
        }
        
    }
}]);

app.controller('geoCtrls.fsWidget',['$scope','$window', 'limitToFilter', '$http', 'rPlace', function($scope, $window, limitToFilter, $http, rPlace){
    // http://localhost:8090/api/place/fs/search/?latlon=34.693738,135.502165
    
    $scope.geoInfo.selectedPlace = null;

    $scope.$watch('geoInfo.data', function(){
        var latlon = $scope.getLatlon();
        if ($scope.geoInfo.data) {
            $scope.geoInfo.loading = true;
        }
        var deferred = rPlace.getData({latlon: latlon, radius: 1000, section: 'topPicks'});
        deferred.then(function(places){
            $scope.geoInfo.places = places.models;
            $scope.geoInfo.loading = false;
        })
    });

}]);

app.controller('geoCtrls.placeItem',['$scope','$window', 'limitToFilter', '$http', 'utils', function($scope, $window, limitToFilter, $http, utils){
    // https://api.instagram.com/v1/locations/search
    var INST_TOKEN = '19342402.1fb234f.6afd663e3d5546b9b9f1fa930888c5a2';

    $scope.onClick = function(){
        $scope.geoInfo.selectedPlace = $scope.place;
        var para = {
            access_token: INST_TOKEN,
            foursquare_v2_id: $scope.place.fid,
            callback: 'JSON_CALLBACK'
        }
        var serialPara = utils.serialize(para)
        
        $http.jsonp('https://api.instagram.com/v1/locations/search?'+serialPara).then(function(r){
            var data = r.data.data;

            if (data.length) {
                var instagramId = data[0].id;
                $http.jsonp('https://api.instagram.com/v1/locations/'+instagramId+'/media/recent?'+serialPara).then(function(response){
                    $scope.geoInfo.instImages = response.data.data;
                });
            }
        });

        $http.get('/api/place/fs/'+$scope.place.fid+'/photos/').success(function(data){
            if (data.success) {
                $scope.geoInfo.fsPhotos = data.response;
            }
        });
    }
    

}]);




app.controller('geoCtrls.geoSearchWidget',['$scope','$window', 'limitToFilter', '$http', 'utils', function($scope, $window, limitToFilter, $http, utils){
    // http://maps.googleapis.com/maps/api/geocode/json?address=Taipei&sensor=true

    $scope.query = '';
    $scope.loading = false;

    this.search = $.debounce(200, function(e){
        if ($scope.loading) {
            return;
        }
        $scope.$apply();
        $scope.loading = true;
        var para = {
            address: $scope.query,
            sensor: true
        };

        $scope.$apply(function(){
            $http.get('http://maps.googleapis.com/maps/api/geocode/json?callback=JSON_CALLBACK&'+utils.serialize(para)).then(function(r){
                var data = r.data;
                $scope.geoInfo.data = data.results.length ? data.results[0]: null;
                $scope.loading = false;
            });
        })
    })

}]);
