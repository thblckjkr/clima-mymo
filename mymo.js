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

 /** EXIT HANDLER **/
function exitHandler(info, err) {
   console.log(info.method, "Succesfull end"); 
   if (info.exit){
      zongji.stop();
      process.exit();
   }
}

//Do something when app is closing
process.on('exit', exitHandler.bind(null,{ method : 'exit'}));

// Catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, { method: 'SIGINT', exit: true }));

// Catches "kill pid" (for example: nodemon restart)
process.on('SIGTERM', exitHandler.bind(null, { method: 'SIGTERM', exit: true }));
process.on('SIGUSR1', exitHandler.bind(null, { method: 'SIGUSR1', exit: true }));
process.on('SIGUSR2', exitHandler.bind(null, { method: 'SIGUSR2', exit: true }));

// Catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(null, { method: 'uncaughtException', exit: true }));
/** EXIT HANDLER **/