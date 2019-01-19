// const DataQA = require('../dataqa');

var parser = function(){
   this.parse = function(data){
      // You can call dataQA from here
      // qa = new DataQA();

      if(typeof data.rows === "undefined" ) {
         console.log("Dropping package because is not a transaction");
         return ;
      }

      let info = data.rows[0];
      console.log(data.constructor.name);
      if( typeof info.before !== "undefined" && typeof info.after !== "undefined"){
         // It's an update!
      }else{
         // It's an insert!
      }
   }
}

module.exports = parser;