// const DataQA = require('../dataqa');

var parser = function(){
   this.parse = function(data){
      // You can call dataQA from here
      // qa = new DataQA();

      if(typeof data.rows === "undefined" ) {
         console.log("Dropping package because not have rows");
         return ;
      }

      let info = data.rows[0];
      switch( data.constructor.name ){
         case "WriteRows":
            // On Insert
            console.log("Inserted data", JSON.stringify(info).slice(0, 100)) ;
            break;
         case "UpdateRows":
            // On Update
            console.log("Updated data", JSON.stringify(info).slice(0, 100)) ;
            break;
         default:
            // It's not an update nor delete, so...
            console.log("Dropping package because is not a transaction");
            break;
      }
   }
}

module.exports = parser;