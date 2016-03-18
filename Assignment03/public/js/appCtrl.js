app.controller('AppCtrl', function ($scope, $rootScope, $cookies, $location, Model) {
    $scope.menuOpen = false;

    $scope.closeMenu = function(){
        $scope.menuOpen = false;
    }

    $scope.toggleMenu = function(){
        if($scope.menuOpen){
            $scope.menuOpen = false;
        } else {
            $scope.menuOpen = true;
        }
    }

    $scope.loggedIn = function(){
        if($rootScope.loggedInUser == undefined){
            return false;
        } else {
            return true;
        }
    }

    $scope.logout = function(){
        delete $rootScope.loggedInUser;
        $cookies.remove("user");
        $scope.closeMenu();
        $location.path("/login");
    }

    $scope.loggedInUser = function(){
        return $rootScope.loggedInUser;
    }
});