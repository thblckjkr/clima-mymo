const fs = require('fs');

var logger = function(){
   this.log = function(){
      fs.writeFileSync('./logs/event.json', JSON.stringify(evt));
   }
}
module.exports = logger;