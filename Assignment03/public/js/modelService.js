app.factory('Model', function ($http) {
	var trendingTopics = [];

	this.getPopular = function(){
		$http.get("/api/trending")
	  	.then(function success(response) {
	  		// console.log("Success!");
	  		// console.log(response.data);
	  		trendingTopics = response.data;
	    }, function error(response) {
	    	console.log("Error!");
	    	console.log(response.data);
	    });
	}

	this.getTrendingTopics = function(){
		if(trendingTopics.length > 0){
			return trendingTopics[0]["trends"];
		}
	}

	return this;
});