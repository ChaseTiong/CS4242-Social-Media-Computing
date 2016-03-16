var fs = require('fs');
var path = require('path');
var express = require('express');
var bodyParser = require('body-parser');
var Twitter = require('twitter');

var app = express();


var twitterClient = new Twitter({
  consumer_key: 'EZU7dkXyANXP81X9FLPClPj3Q',
  consumer_secret: '57HSlTd5t4GRzaWuy4j0QH2angoQrbW9CCqXT8ANDiKm7iWwq8',
  access_token_key: '616422343-QxppVIi6s143vV2yc1KGQk6JV79G0kRK5GzDOOw1',
  access_token_secret: 'zMsu8dBKfkSvz8oWhKaoG4PHt0ptAuEpw7HYl2lNdhNVi'
});

app.set('port', (process.env.PORT || 3000));
app.use('/', express.static(path.join(__dirname, 'public')));
app.use('/libraries', express.static(path.join(__dirname, 'node_modules')));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.use(function(req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Cache-Control', 'no-cache');
    next();
});

var lastRequest = null;
var globalTrends;

app.get('/api/trending', function(req, res){

  console.log("Incoming request for /api/trending");
  var currentTime = new Date();

  if(lastRequest != null){
    console.log("Calculating time difference!");
    var timeDiff = (currentTime-lastRequest)/1000;
  } else {
    console.log("First request since server started.");
    var timeDiff = 300;
  }

  console.log("Time difference set to "+timeDiff);
  

  if((timeDiff >= 300)){
    console.log("Time diff high enough for new request to be made");

    var params = {id: 1};
    twitterClient.get('trends/place', params, function(error, trends, response){
      if(error){
        // console.log("Request failed");
        console.log(error.body);
        res.json(error.body);
      } else {
        // console.log("Successful request");
        globalTrends = trends;
        res.json(trends);
        lastRequest = currentTime;
      }
    })
  } else {
    res.json(globalTrends)
  }
});


app.listen(app.get('port'), function() {
  console.log('Server started: http://localhost:' + app.get('port') + '/');
});