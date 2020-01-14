# Simple information importer
# This one is dirty AF [@thblckjkr]

import json
import pymysql.cursors
import pymongo
import requests

# xml requests
from lxml import objectify

# Import configuration
with open('../config/config.json') as json_file:
   config = json.load(json_file)

class uploader:

   def __init__(self, db):
      # Get a database and load the corresponding everything from the public XML
      self.name = ""
      self.loadXML(db)
      self.db = db

      self.conn = pymysql.connect(
         host = config['mysql']['host'],
         user = config['mysql']['username'],
         passwd = config['mysql']['password']
      )

      host = "148.210.68.163" # pruebas
      puerto = "27017"
      bd = "Clima"

      cliente = pymongo.MongoClient("mongodb://{}:{}".format(host, puerto))

      self.mon = cliente[bd]

   # Load defaults from server
   def loadXML(self, db):
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
      sql = 'SELECT ' + sql + ' FROM archive order by dateTime DESC'
      print ('sql para estacion \n', sql)

      with self.conn.cursor() as cursor:
         cursor.execute('use ' + self.db)
         cursor.execute(sql)

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
            i = i + 1
            if i == 100: break

            self.insert(temp)
            print("Inseted", i)
            
         self.conn.close()
         return True

   def insert(self, datos):
      var = self.mon["archive"].insert_one(datos).inserted_id
      return var
      
databaseName = input("¿Que base de datos desea importar? ")
# databaseName = "Estacion26"
u = uploader(databaseName)

# TODO: Remove
temp = input("Presione ctrl + c  para terminar")

data = u.loadSQL()