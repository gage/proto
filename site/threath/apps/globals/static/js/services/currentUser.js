app.service('currentUser', ['initData', function(initData){
    this.model = initData.currentUser;
    
}]);