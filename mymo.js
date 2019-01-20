var ZongJi = require('zongji');
var Parser = require('./lib/parser');

const db = require('./database/config.json');

// Link and instanciate the parser for storing the data
var parser = new Parser();

// MySQL credentials [Change here]
var zongji = new ZongJi({
   serverId : db.mysql.serverId,
   host: db.mysql.host,
   user: db.mysql.username,
   password: db.mysql.password
});

// Each change to the replication log results in an event
zongji.on('binlog', function(evt) {
   console.log( new Date(), "Event detected");
   // Send the event info to a parser
   parser.parse(evt);
});

// Binlog must be started, optionally pass in filters
// tablemap is important to catch all the other events
zongji.start({
  includeEvents: ['tablemap', 'writerows', 'updaterows', 'deleterows']
});

// Stop process on SIGINT (Remember to add the another one's)
process.on('SIGINT', function() {
   console.log('Got SIGINT.');
   zongji.stop();
   process.exit();
 });