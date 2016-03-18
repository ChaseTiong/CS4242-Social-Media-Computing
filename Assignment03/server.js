var fs = require('fs');
var path = require('path');
var express = require('express');
var bodyParser = require('body-parser');
var Twitter = require('twitter');

var app = express();
var lastRequest = null;
var TRENDSFILE = path.join(__dirname, 'trends.json');

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

app.get('/api/trending', function(req, res){
  var updateThreshold = 1800;
  console.log("Incoming request for /api/trending for WOEID " + req.query.WOEID);
  
  var currentTime = new Date();

  // Read JSON file with previous trends
  fs.readFile(TRENDSFILE, function(err, data) {
    if (err) {
      console.log("Failed to read "+TRENDSFILE);
      console.error(err);
      process.exit(1);
    }

    // Parse previous data
    var previousData = JSON.parse(data);

    if(previousData["trends"][req.query.WOEID] == undefined){
      // No previous record for given WOEID
      console.log("No previous records exist");
      var timeDiff = updateThreshold;
    } else {
      // Previous records exists for given WOEID
      console.log("Previous records exist");
      var lastRequest = new Date(previousData["trends"][req.query.WOEID]["lastRequest"]);
      var timeDiff = (currentTime-lastRequest)/1000;
    }

    console.log("Time difference set to "+timeDiff);
    
    if(timeDiff >= updateThreshold){
      console.log("Time diff high enough for new request to be made");

      var params = {id: req.query.WOEID};
      twitterClient.get('trends/place', params, function(error, trends, response){
        if(error){
          console.log("Twitter request failed!");
          console.log(error);
          res.json(error);
        } else {
          console.log("Request successful!");
          previousData["trends"][req.query.WOEID] = {};
          previousData["trends"][req.query.WOEID]["lastRequest"] = new Date();
          previousData["trends"][req.query.WOEID]["trends"] = trends;

          console.log("Writing data to JSON-file");
          // WRITE FILE
          fs.writeFile(TRENDSFILE, JSON.stringify(previousData, null, 4), function(err){
            if(err){
              console.log("Writing to file failed!");
              console.error(err);
              process.exit(1);
            }
            console.log("File saved successfully!");
            res.json(trends);
          });
        }
      })
    } else {
      // TIMEDIFF NOT BIG ENOUGH
      console.log("Timediff not big enough, returning previously saved data");
      res.json(previousData["trends"][req.query.WOEID]["trends"]);
    }
  });
});


app.listen(app.get('port'), function() {
  console.log('Server started: http://localhost:' + app.get('port') + '/');
});