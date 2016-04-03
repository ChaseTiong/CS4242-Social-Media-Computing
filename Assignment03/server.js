var fs = require('fs');
var path = require('path');
var express = require('express');
var bodyParser = require('body-parser');
var Twitter = require('twitter');
var MySql = require('mysql');
var PythonShell = require('python-shell');

var app = express();
var lastRequest = null;
var TRENDSFILE = path.join(__dirname, 'trends.json');
var TWEETSFILE = path.join(__dirname, 'tweets.json');

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

app.post('/api/register', function(req, res){
  var userData = JSON.parse(req.query.user);
  var returnObject = {duplicateUsers: "Unknown", successfulUpdate: false};

  var statement = "SELECT * FROM users WHERE username = "+dbConnection.escape(userData.name)+";";
  dbConnection.query(statement, function(err, result) {
    if(result.length > 0){
      returnObject.duplicateUsers = true;
      res.json(returnObject);
    } else {
      returnObject.duplicateUsers = false;

      var statement = "INSERT INTO users (username, password) VALUES ("+dbConnection.escape(userData.name)+", "+dbConnection.escape(userData.password)+");";
      var getUserIDQuery = "SELECT user_id FROM users WHERE username = "+dbConnection.escape(userData.name)+" AND password = "+dbConnection.escape(userData.password)+";";

      dbConnection.query(statement, function(err, result){
        if(err){
          console.log("ERROR 1!");
          console.log(err);
          returnObject.successfulUpdate = false;
        } else {
          console.log(result);
          dbConnection.query(getUserIDQuery, function(err, result){
            if(err){
              console.log("ERROR 2!");
              console.log(err);

            } else {
              returnObject["user_id"] = result[0]["user_id"];
              returnObject.successfulUpdate = true;
            }
            res.json(returnObject);
          })
        }   
      });
    }
  });
});

app.post("/api/login", function(req, res){
  var credentials = JSON.parse(req.query.credentials);
  var statement = "SELECT * FROM users WHERE username = "+dbConnection.escape(credentials.username)+" and password = "+dbConnection.escape(credentials.password)+";";

  dbConnection.query(statement, function(err, result){
    if(err){
      console.log(err);
      res.json(err);
    } else {
      if(result.length == 1){
        res.json({success: true, user_id: result[0]["user_id"]});
      } else {
        res.json({success: false});
      }
    }
  })
});

app.get('/api/tweets', function(req, res){
  console.log("Incoming request for ",req.query.q, " tweets");
  var params = {q: req.query.q, count:100, type:"popular", lang:"en"};
  twitterClient.get('search/tweets', params, function(error, tweets, response){
    // if (error) throw error;
    if(error){
      res.json(error)
    } else {
      console.log("Fetched ",tweets.statuses.length, " tweets from twitter, inserting into database.");

      var query = "INSERT IGNORE INTO tweets(id, created_at, lang, favourite_count, retweet_count, text) VALUES ";
      var stringifiedTweets = []
      for (tweet in tweets.statuses){
        if(tweets.statuses[tweet]["retweeted_status"] == undefined){
          var currentTweet = tweets.statuses[tweet];
        } else {
          var currentTweet = tweets.statuses[tweet]["retweeted_status"];
        }

        stringifiedTweets.push(JSON.stringify(currentTweet["text"]));

        query += "("+currentTweet["id_str"]+",'"+new Date().toISOString(currentTweet["created_at"]).slice(0, 19).replace('T', ' ')+"','"+currentTweet["lang"]+"',"+currentTweet["favorite_count"]+","+currentTweet["retweet_count"]+","+dbConnection.escape(currentTweet["text"])+")";

        if(tweet != (tweets.statuses.length-1)){
          query += ",";
        } else {
          query += ";";
        }
      }

      dbConnection.query(query, function(err, result){
        if(err) throw err;
        console.log("Tweets successfully saved to database!");
        console.log(result);
      });

      var options = {
        args: stringifiedTweets
      };

      console.log("Classifying tweets...");
      PythonShell.run("python/classifyTweets.py", options, function(err, result){
        if(err) throw err;
        tweets.labels = result;
        console.log("Tweets classified");
        for(i in tweets.statuses){
          tweets.statuses[i].predicted_sentiment = result[i];
        }
        console.log("Returning ",tweets.statuses.length," tweets");
        res.json(tweets);
      });  
    }
    

  });
});

app.get('/api/trending', function(req, res){
  var updateThreshold = 5400;
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