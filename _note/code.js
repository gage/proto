//======================== Angular ===========================
	// Dependency 
	myApp.filter('reverse', function(Data){ 
		return function(text) {
			return text.split("").reverse().join("") + Data.message;
		}
	}) ;

	// Scope executes functions
	scope.$apply("something()")

	app.controller('AppCtrl', function($scope) {
		$scope.loadMoreTweets = function() {
			alert('');
		}
	})
	app.directive('enter', function(){
		return function(scope, elelment, attrs) {
			element.bind("mouseenter", function(){
				// scope.loadMoreTweets();
				scope.$apply(attrs.enter);
			})
		}
	})

	// ng-include, ng-click
	<div ng-controller="Ctrls.IndexCtrl">
		Hello World
		<br>
		<div ng-include src="template.url"></div>
		<div ng-click="changeUrl()">To main</div>

	</div>

//======================== Backbone ===========================
	
	"stopListening 可以把註冊的事件消掉"
	view.remove() "會去call stopListening"

	// Delegate Event
	view.delegateEvents();
	view.undelegateEvents();


//======================== Console ===========================
	// Grouping debug message
	var user = "jsmith", authenticated = false;
	console.group("Authentication phase");
	console.log("Authenticating user '%s'", user);
	// authentication code here...
	if (!authenticated) {
	    console.log("User '%s' not authenticated.", user)
	}
	console.groupEnd();

	// TIME
	console.time("Array initialize");
	var array= new Array(1000000);
	for (var i = array.length - 1; i >= 0; i--) {
	    array[i] = new Object();
	};
	console.timeEnd("Array initialize");



//======================== General ===========================
// Keypress Code
	var code = (e.keyCode ? e.keyCode : e.which);
	if (code == 13){
		// Enter
	    // Do something
	};

// Date
	new Date() // current date and time
	new Date(milliseconds) //milliseconds since 1970/01/01
	new Date(dateString)
	new Date(year, month, day, hours, minutes, seconds, milliseconds)

// Convert
	parseInt('String'); 
	parseFloat('String'); 

// json
	// Django
	{{collection|safe}}
	// html
	JSON.parse(collection)

// Encode URL
	var myOtherUrl = "http://example.com/index.html?url=" + encodeURIComponent(myUrl);

// Url parameters
	function getQueryVariable(url, variable) {
	    var query = url.split('?')[1];
	    if (!query) {
	    	return '';
	    }
	    var vars = query.split('&');
	    for (var i = 0; i < vars.length; i++) {
	        var pair = vars[i].split('=');
	        if (decodeURIComponent(pair[0]) == variable) {
	            return decodeURIComponent(pair[1]);
	        }
	    }
	    console.log('Query variable %s not found', variable);
	};