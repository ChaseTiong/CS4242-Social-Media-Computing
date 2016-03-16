app.controller('AppCtrl', function ($scope, Model) {
	$scope.getTwitterData = function(){
		Model.getPopular();
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
    			console.log(geography)
    		});
		}
    });

    // // Pure JavaScript
    // window.addEventListener('resize', function() {
    //     map.resize();
    // });

    // // Alternatively with d3
    // d3.select(window).on('resize', function() {
    //     map.resize();
    // });

    // Alternatively with jQuery
    $(window).on('resize', function() {
       map.resize();
	});
	}
});