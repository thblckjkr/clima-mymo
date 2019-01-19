var ZongJi = require('zongji');
var Parser = require('./lib/parser');

var parser = new Parser();

var zongji = new ZongJi({
   host: "localhost",
   user: "maxwell",
   password: "password"
});

// Each change to the replication log results in an event
zongji.on('binlog', function(evt) {
   console.log( new Date(), "Event detected");
   // Send the event info to a parser
   parser.parse(evt);
});

// Binlog must be started, optionally pass in filters
zongji.start({
  includeEvents: ['tablemap', 'writerows', 'updaterows', 'deleterows']
});

// Stop process on SIGINT (Remember to add the another one's)
process.on('SIGINT', function() {
   console.log('Got SIGINT.');
   zongji.stop();
   process.exit();
 });