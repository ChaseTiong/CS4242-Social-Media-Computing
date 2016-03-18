app.controller('AppCtrl', function ($scope, Model) {
	$scope.getTwitterData = function(query){
		Model.getPopular(query);
	}

    $scope.loadingTrends = function(){
        return Model.loadingTrends();
    }

    $scope.errorStatus = function(){
        return Model.getErrorStatus();
    }

	$scope.trendingTopics = function(){
		return Model.getTrendingTopics();
	}

	$scope.initializeMap = function(){
		var map = new Datamap({
        element: document.getElementById('worldMap'),
        responsive: true,
        done: function(datamap) {
    		datamap.svg.selectAll('.datamaps-subunit').on('click', function(geography) {
                // Click Event
                Model.getPopular(geography.properties.name);
    		});
		}
    });

    $scope.showingTrends = function(){
        return Model.activeTopic();
    }

    // Alternatively with jQuery
    $(window).on('resize', function() {
       map.resize();
	});
	}
});