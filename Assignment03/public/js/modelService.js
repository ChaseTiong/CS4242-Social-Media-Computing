app.factory('Model', function ($http, $resource) {
	var trendingTopics = {
		WOEID: 1,
		name: "World",
		trends: []
	};

	var selectedTopic = {};
	var topTweets = [];
	var sentiments = [];

	var errorStatus = false;
	var loadingTrends = false;
	var loadingTweets = false;

	this.partialTopicUpdate = function(name){
		trendingTopics.name = name;
		trendingTopics.trends = [];
	}

	this.clearTweets = function(){
		topTweets = [];
	}

	this.topTweetsForCurrentTopic = function(){
		return topTweets;
	}

	this.setSelectedTopic = function(topic){
		console.log(topic)
		selectedTopic = topic;
	}

	this.getSelectedTopic = function(){
		return selectedTopic;
	}

	this.getErrorStatus = function(){
		return errorStatus;
	}

	this.loadingTrends = function(){
		return loadingTrends;
	}

	this.loadingTweets = function(){
		return loadingTweets;
	}

	this.activeRegion = function(){
		return trendingTopics["name"];
	}

	this.getTrendingTopics = function(){
		if(trendingTopics["trends"].length > 0){
			return trendingTopics["trends"];
		} 
	}

	this.getSentiments = function(){
		return sentiments;
	}

	this.getPopular = function(query){
		this.partialTopicUpdate(query);
		
		var appID = "dj0yJmk9YmFya3J1OVU0TU1NJmQ9WVdrOVRIbE1PR3B0TTJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD03NA--";
		loadingTrends = query;
		errorStatus = false;
		$http.get("http://where.yahooapis.com/v1/places.q('"+query+"')?appid="+appID+"--").then(
			function success(response){
				// console.log("WOEID request successful for query '"+query+"', returned "+response.data.places.place[0].woeid);
				if(response.data.places.count == 0){
					// Error handling
					errorStatus = "No locations matching given query.";
					loadingTrends = false;
				} else {
					var activeWOEID = response.data.places.place[0].woeid;
					// console.log(response.data.places.place[0]);
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
				}

			}, function error(response){
				console.log("Failed to get WOEID");
				console.log(response.data);
			}
		);
	}


	this.getTopTweets = function(){
		loadingTweets = true;
		sentiments = [];
		var params = {
			url: "/api/tweets",
			method: "GET",
			params: {q: selectedTopic["query"]}
		}

		$http(params).then(function success(response){
			// Show original tweets instead of retweets
			for(s in response.data.statuses){
				if(response.data.statuses[s].retweeted_status){
					response.data.statuses[s] = response.data.statuses[s].retweeted_status;
					response.data.statuses[s].predicted_sentiment = response.data.labels[s];
				} 
			}

			// Filter out duplicates (since two Twitter users could have retweeted the same tweet)
			var ids = [];
			var removeIndexes = [];
			
			// Iterate through the statuses and find the indexes of the tweets with duplicate IDs.
			for(s in response.data.statuses){
				if(ids.indexOf(response.data.statuses[s].id) != -1){
					removeIndexes.push(s);
				} else {
					ids.push(response.data.statuses[s].id)
				}
			}

			// Loop through the indexes of the tweets to be removed from back to front
			for(var i = removeIndexes.length; i>0; i--){
				var removeAtIndex = parseInt(removeIndexes[i], 10);
				if(removeAtIndex){
					response.data.statuses.splice(removeAtIndex,1);
					response.data.labels.splice(removeAtIndex,1);
				}
			}

			// Assign data to model
			topTweets = response.data;
			sentiments = response.data.labels;
			loadingTweets = false;
		}, function error(response){
			console.log(response);
			loadingTweets = false;
		});
	}

	return this;
});