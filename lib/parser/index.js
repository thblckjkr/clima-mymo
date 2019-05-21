var parser = function(){
   this.parse = function(data){
      if(typeof data.rows === "undefined" ) {
         console.log("Dropping package because it does not have rows");
         return ;
      }
      for(let i = 0; i < data.rows.length; i++){
         parserow(data.rows[i], data, data.constructor.name);
      }
      
   }
   // Private row 
   var parserow = function(info, data, action){
      switch( action ){
         case "WriteRows":
            // On Insert
            console.log(
               "Inserted data",
               data.timestamp,
               data.tableMap[data.tableId].parentSchema,
               data.tableMap[data.tableId].tableName,
               info['dateTime']
            ) ;
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