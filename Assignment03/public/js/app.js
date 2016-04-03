var app = angular.module('cs4242', ['ngRoute', 'ngResource', 'ngCookies']);

app.config(['$routeProvider',
	function($routeProvider) {
		$routeProvider.
		when('/', {
			templateUrl: 'partials/map.html',
			controller: 'mapCtrl',
			activeTab: 'home'
		}).
		when('/login', {
			templateUrl: 'partials/login.html',
			controller: 'LoginCtrl',
			activeTab: 'login'
		}).
		when('/register', {
			templateUrl: 'partials/register.html',
			controller: 'LoginCtrl',
			activeTab: 'register'
		}).
		when('/viewStats', {
			templateUrl: 'partials/topic.html',
			controller: 'topicCtrl',
			activeTab: 'topic'
		}).
		otherwise({
			redirectTo: '/'
		})
	}
]).
run(function($rootScope, $location, $cookies){
	$rootScope.$on( "$routeChangeStart", function(event, next, current) {
		if(($cookies.get("username") != undefined) && ($cookies.get("user_id") != undefined)){
			$rootScope.loggedInUser = {username: $cookies.get("username"), user_id: $cookies.get("user_id")};
		}

		if($rootScope.loggedInUser == undefined){
			if(next["$$route"]["activeTab"] != "register"){
				$location.path("/login");
			}
		} else {
			if(next["$$route"] != undefined){
				if((next["$$route"]["activeTab"] == "login") || (next["$$route"]["activeTab"] == "register")){
					$location.path("/map");
				}
			}
		}

    });
});