app.controller('LoginCtrl', function ($scope, Model, $location, $cookies, $http) {
    $scope.user = {
        name: "",
        password: "",
        repeatedPassword: ""
    };

    $scope.errorStatus = false;
    $scope.loadingRegistration = false;

    $scope.checkLogin = function(){
        var sendRequest = true;
        var requestedUsername = $scope.user.name;
        if($scope.user.password.length == 0) sendRequest = false;
        if($scope.user.name.length == 0) sendRequest = false;

        if(sendRequest){
            var params = {
                url: "/api/login",
                method: "POST",
                params: {
                    credentials: {
                        username: $scope.user.name.toLowerCase(),
                        password: $scope.user.password
                    }
                }
            }

            $http(params).then(function success(response){
                console.log(response);
                if(response.data.success){
                    console.log("Successful login!");
                    
                    $scope.setUserCookie(requestedUsername, response.data.user_id);
                    $location.path("/");
                } else {
                    console.log("Failed login!");
                    $scope.errorStatus = "Login failed";
                }
            }, function error(response){
                console.log(response);
                $scope.errorStatus = "Login failed";
            })
        } else {
            $scope.errorStatus = "Unable to login";
        }
    }

    $scope.register = function(){
        $scope.errorStatus = false; 
        $scope.loadingRegistration = true;
        if($scope.user.password != $scope.user.repeatedPassword) $scope.errorStatus = "Passwords doesn't match.";
        if($scope.user.password.length < 3) $scope.errorStatus = "Password must be at least 3 characters long.";
        if($scope.user.password.length == 0) $scope.errorStatus = "Please enter a password.";
        if($scope.user.name.length < 5) $scope.errorStatus = "Username must be at least 5 characters long.";
        if($scope.user.name.length == 0) $scope.errorStatus = "Please enter a username.";

        if(!$scope.errorStatus){
            var params = {
                url: "/api/register",
                method: "POST",
                params: {
                    user: {
                        name: $scope.user.name.toLowerCase(),
                        password: $scope.user.password
                    }
                }
            };

            $http(params).then(function success(response){
                console.log(response);
                if(!response.data.successfulUpdate) $scope.errorStatus = "Database update failed.";
                if(response.data.duplicateUsers) $scope.errorStatus = "Username is already taken.";

                if(!$scope.errorStatus){
                    console.log("Registration successful!");
                    $scope.setUserCookie($scope.user.name, response.data.user_id);
                    $location.path("/");
                }
                $scope.loadingRegistration = false;
            }, function error(response){
                $scope.errorStatus = response;
                $scope.loadingRegistration = false;
            });
        } else {
            $scope.loadingRegistration = false;
        }
    }

    $scope.goToRegister = function(){
        $location.path("/register");
    }

    $scope.goToLogin = function(){
        $location.path("/login");
    }

    $scope.setUserCookie = function(username, userID){
        $cookies.put("user_id", userID);
        $cookies.put("username", username);
    }
});

app.controller('mapCtrl', function ($scope, Model) {
    $scope.userQuery = "";

    $scope.updateSelectedTopic = function(topic){
        Model.setSelectedTopic(topic);
    }
    $scope.getTwitterData = function(query){
        Model.getPopular(query);
    }

    $scope.trendingTopics = function(){
        return Model.getTrendingTopics();
    }

    $scope.loadingTrends = function(){
        return Model.loadingTrends();
    }

    $scope.errorStatus = function(){
        return Model.getErrorStatus();
    }

    $scope.showingTrends = function(){
        return Model.activeRegion();
    }

    $scope.initializeMap = function(){
        var map = new Datamap({
        element: document.getElementById('worldMap'),
        responsive: true,
        done: function(datamap) {
            datamap.svg.selectAll('.datamaps-subunit').on('click', function(geography) {
                Model.getPopular(geography.properties.name);
            });
        }
        });
    }

    $(window).on('resize', function() {
        try{
            map.resize()
        } catch(e) {}
    });

    $("#mainSearch").keyup(function (e) {
        if (e.keyCode == 13) {
            if($scope.userQuery.length != 0){
                $scope.getTwitterData($scope.userQuery);
                $scope.userQuery = "";
            }
        }
    });


    var init = function(){
        $scope.initializeMap();
        $scope.getTwitterData(Model.activeRegion());
        $("#mainSearch").focus();
    }

    init();
});

app.controller('topicCtrl', function ($scope, Model, $location) {
    $scope.Math = window.Math;

    $scope.activeTopic = function(){
        return Model.getSelectedTopic();
    }

    if($scope.activeTopic()["name"] == undefined){
        $location.path("/");
    }

    $scope.topTweets = function(){
        return Model.topTweetsForCurrentTopic()["statuses"];
    }

    $scope.loadingTweets = function(){
        return Model.loadingTweets();
    }

    $scope.sentiments = function(){
        var sentiments = Model.getSentiments();
        var stats = {
            positive: {
                count: 0,
                name: "Positive"
            },
            negative: {
                count: 0,
                name: "Negative"
            },
            neutral: {
                count: 0,
                name: "Neutral"
            },
            irrelevant: {
                count: 0,
                name: "Irrelevant"
            },
            total: {
                count: 0,
                name: "All"
            }
        };

        for (sentiment in sentiments){
            stats[sentiments[sentiment]].count += 1;
            stats.total.count += 1;
        };

        return stats;
    }

    $scope.filterOptions = $scope.sentiments();


    $scope.tweetFilter = function(tweet){
        var currentFilter = $scope.showResultType.toLowerCase();
        if(currentFilter == "all"){
            return true;
        } else if(tweet.predicted_sentiment == currentFilter){
            return true;
        } else {
            return false;
        }
    }

    var init = function(){
        Model.clearTweets();
        Model.getTopTweets();
        $scope.showResultType = "All";
    }

    init();
});