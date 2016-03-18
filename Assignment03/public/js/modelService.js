app.factory('Model', function ($http, $resource) {
	var trendingTopics = {
		WOEID: 1,
		name: "World",
		trends: []
	};

	var errorStatus = false;
	var loadingTrends = false;

	this.getErrorStatus = function(){
		return errorStatus;
	}

	this.loadingTrends = function(){
		return loadingTrends;
	}

	this.activeTopic = function(){
		return trendingTopics["name"];
	}

	this.getTrendingTopics = function(){
		if(trendingTopics["trends"].length > 0){
			return trendingTopics["trends"];
		} 
	}

	this.getPopular = function(query){
		var appID = "dj0yJmk9YmFya3J1OVU0TU1NJmQ9WVdrOVRIbE1PR3B0TTJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD03NA--";
		loadingTrends = query;
		errorStatus = false;
		$http.get("http://where.yahooapis.com/v1/places.q('"+query+"')?appid="+appID+"--").then(
			function success(response){
				// console.log("WOEID request successful for query '"+query+"', returned "+response.data.places.place[0].woeid);
				var activeWOEID = response.data.places.place[0].woeid;

				var params = {
					url: "/api/trending",
					method: "GET",
					params: {WOEID: activeWOEID}
				};

				$http(params).then(function success(response){
					trendingTopics["WOEID"] = activeWOEID;
					trendingTopics["name"] = query;
					
					// Response includes error code
					if(response.data[0]["code"] != undefined){
						console.log(response.data[0]["code"]);

						if(response.data[0]["code"] == 34){
							console.log("Twitter does not provide data for this region");
							errorStatus = "Twitter does not provide data for this region, sorry about that! Feel free to click somewhere else on the map!";
							trendingTopics["trends"] = [];
						} else if (response.data[0]["code"] == 88) {
							console.log("Twitter API rate limit exceeded");
							errorStatus = "Twitter API rate limit exceeded, try again in a few minutes!";
							trendingTopics["trends"] = [];
						} else {
							console.log("Unknown error");
							errorStatus = "Unknown error";
							trendingTopics["trends"] = [];
						}

					// Response does not include error code
					} else {
						trendingTopics["trends"] = response.data[0]["trends"];
						errorStatus = false;

					}

					loadingTrends = false;

				}, function error(response){
					console.log("Error while retrieving twitter data!");
					console.log(response.data);

				});

			}, function error(response){
				console.log("Failed to get WOEID");
				console.log(response.data);
			}
		);
	}

	return this;
});