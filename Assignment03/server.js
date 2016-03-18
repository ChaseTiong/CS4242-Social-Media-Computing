var fs = require('fs');
var path = require('path');
var express = require('express');
var bodyParser = require('body-parser');
var Twitter = require('twitter');
var MySql = require('mysql');

var app = express();
var lastRequest = null;
var TRENDSFILE = path.join(__dirname, 'trends.json');

var twitterClient = new Twitter({
  consumer_key: 'EZU7dkXyANXP81X9FLPClPj3Q',
  consumer_secret: '57HSlTd5t4GRzaWuy4j0QH2angoQrbW9CCqXT8ANDiKm7iWwq8',
  access_token_key: '616422343-QxppVIi6s143vV2yc1KGQk6JV79G0kRK5GzDOOw1',
  access_token_secret: 'zMsu8dBKfkSvz8oWhKaoG4PHt0ptAuEpw7HYl2lNdhNVi'
});

var dbConnection = MySql.createConnection({
  port: 8889,
  host: "localhost",
  database: "CS4242",
  user: "root",
  password: "root"
});

dbConnection.connect(function(err){
  if(err) console.log(err);
})

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

app.post('/api/register', function(req, res){
  var userData = JSON.parse(req.query.user);
  var returnObject = {duplicateUsers: "Unknown", successfulUpdate: false};

  var statement = "SELECT * FROM users WHERE username = '"+userData.name+"';";
  dbConnection.query(statement, function(err, result) {
    if(result.length > 0){
      returnObject.duplicateUsers = true;
      res.json(returnObject);
    } else {
      returnObject.duplicateUsers = false;

      var statement = "INSERT INTO users (username, password) VALUES ('"+userData.name+"', '"+userData.password+"');";
      dbConnection.query(statement, function(err, result){
        if(err){
          console.log(err);
          returnObject.successfulUpdate = false;
        } else {
          // console.log(result);
          returnObject.successfulUpdate = true;
        }
        res.json(returnObject);
      });
    }
  });
});

app.post("/api/login", function(req, res){
  var credentials = JSON.parse(req.query.credentials);
  var statement = "SELECT count(*) FROM users WHERE username = "+dbConnection.escape(credentials.username)+" and password = "+dbConnection.escape(credentials.password)+";";

  dbConnection.query(statement, function(err, result){
    if(err){
      console.log(err);
      res.json(err);
    } else {
      if(result[0]['count(*)']==1){
        res.json({success: true});
      } else {
        res.json({success: false});
      }
    }
  })
});

app.get('/api/tweets', function(req, res){
  var params = {q: req.query.q, count:15, type:"popular"};
  twitterClient.get('search/tweets', params, function(error, tweets, response){
    if(error){
      console.log(error);
    }
    res.json(tweets);
  });
});

app.get('/api/trending', function(req, res){
  var updateThreshold = 1800;
  // console.log("Incoming request for /api/trending for WOEID " + req.query.WOEID);
  
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