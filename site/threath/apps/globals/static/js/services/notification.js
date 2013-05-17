app.factory('notification', ['$q','$http','$timeout',function($q,$http,$timeout){
    notification = {};

    browserSupportNotification = function() {
        return window.webkitNotifications;
    }

    notification.requestPermission = function() {
        if (!browserSupportNotification()) {
            return;
        }
        // 0 means we have permission to display notifications
        if (window.webkitNotifications.checkPermission() == 0) {
            return;
        } else {
            window.webkitNotifications.requestPermission();
        }
    }

    notification.Notify = function(image, title, content) {
        if (!browserSupportNotification()) {
            return;
        }
        if (window.webkitNotifications.checkPermission() == 0) {
            return window.webkitNotifications.createNotification(image, title, content);
        }
        else {
            window.webkitNotifications.requestPermission();
        }
    }

    notification.showNotify = function(image, title, content){
        var notifyMsg = notification.Notify(image, title, content);
        if (notifyMsg) {
            notifyMsg.onclick = function(){
                window.focus();
                this.cancel();
            };
            notifyMsg.show();
        }
    }

    return notification;
}]);





