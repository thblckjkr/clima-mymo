// const DataQA = require('../dataqa');

var parser = function(){
   this.parse = function(data){
      // You can call dataQA from here
      // Also, you could prevent to update if something just with a flag
      // qa = new DataQA();

      if(typeof data.rows === "undefined" ) {
         console.log("Dropping package because not have rows");
         return ;
      }
      for(let i = 0; i < data.rows.length; i++){
         parserow(data.rows[0], data.constructor.name);
      }
      
   }
   // Private row 
   var parserow = function(info, action){
      switch( action ){
         case "WriteRows":
            // On Insert
            console.log("Inserted data", JSON.stringify(info).slice(0, 100)) ;
            break;
         case "UpdateRows":
            // On Update
            console.log("Updated data", JSON.stringify(info).slice(0, 100)) ;
            break;
         case "DeleteRows":
            // On delete
            break;
         default:
            // It's not an update nor delete, so...
            console.log("Dropping package because is not a transaction");
            break;
      }
   }
}

module.exports = parser;