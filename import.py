# Simple information importer
# This one is dirty AF [@thblckjkr]

# Parameters
import sys

import json
import pymysql.cursors
import pymongo
import requests

from utils import UI

# xml requests
from lxml import objectify

# Import configuration
with open('config/config.json') as json_file:
   config = json.load(json_file)

# Init GUI
u = UI()

class uploader:

   def __init__(self, db):
      # Get a database and load the corresponding everything from the public XML
      u.show("Connecting to the database", "info")

      self.name = ""
      self.loadXML(db)
      self.db = db

      self.conn = pymysql.connect(
         host = config['mysql']['host'],
         user = config['mysql']['username'],
         passwd = config['mysql']['password']
      )

      cliente = pymongo.MongoClient( config['mongo']['url'] )

      self.mon = cliente[config['mongo']['dbName']][config['mongo']['collection']]

      u.show("Successfully connected to the database", "success")

   # Load defaults from server
   def loadXML(self, db):
      u.show("Loading XML Schema", "info")
      self.sensores = [ 'dateTime' ]
      # Get XML from URL
      r = requests.get(config['schema']['url'], allow_redirects = False)
      # objectify
      objeto = objectify.fromstring(r.content)

      # Para cada estacion en el archivo
      for item in objeto.Estaciones.Estacion:
         if "".join(item.get("nombre").split(" ")) == db:
            # Generate fields
            self.name = item.get("nombre")
            self.datos = {
               "units": int(item.find("sistemamt").text),
               "interval": int(item.find("intervalo").text),
               "state": 0
            }

            for sensor in item.sensores.iterchildren():
               self.sensores.append( str(sensor.sql) )
            return True

   def loadSQL(self):
      sql = " ,".join(self.sensores)
      sql = 'SELECT ' + sql + ' FROM archive ORDER BY dateTime DESC'

      with self.conn.cursor() as cursor:
         u.show("Executing query", "info")

         cursor.execute('use ' + self.db)
         cursor.execute(sql)

         u.show("Query executed, starting parsing and upload", "success")

         # Obtener una a una toda la informacion
         i = 0
         while True:
            row = cursor.fetchone()
            temp = {
               "station" : self.name,
               "dateTime": row[0],
               "data": {
                  "units": self.datos['units'],
                  "interval": self.datos['interval'],
                  "state": self.datos['state'],
                  "sensor" : {}
               }
            }
            for j in range (len(self.sensores)):
               if self.sensores[j] == "dateTime":
                  continue

               temp["data"]["sensor"][self.sensores[j]] = { "value": row[j] }

            if row == None:
               break
            # Count to break or print usefull info
            i = i + 1
            if i % 1000 == 0:
               print( str(i), sep=",", end='')


            self.insert(temp)
            print(str(i) + ",")
            
         self.conn.close()
         return True

   def insert(self, datos):
      var = self.mon.insert_one(datos).inserted_id
      return var
      
def main(argv):
   
   u.ask("Utilizando colección %s. Presione Ctrl+C para abortar" % config['mongo']['collection'])

   if len(argv) <= 1:
      databaseName = u.ask("¿Que base de datos desea importar?")
      upl = uploader(databaseName)
      temp = input("Presione Ctrl+C para abortar o enter para continuar")
      data = upl.loadSQL()

   else:
      for x in argv[1:]:
         u.show("Cargando base de datos [%s]" % x, "warning")
         upl = uploader(x)
         try:
            data = upl.loadSQL()
         except:
            print("Algun error ha ocurrido, parece ser normal")

if __name__ == "__main__":
    main(sys.argv)
