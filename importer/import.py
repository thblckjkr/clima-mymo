# Simple information importer
# This one is dirty AF [@thblckjkr]

import json
import pymysql.cursors
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

            for sensor in item.sensores.iterchildren():
               self.sensores.append( str(sensor.sql) )
            return True

   def loadSQL(self):
      dataset = []
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
               "sensor": []
            }
            for j in range (len(self.sensores)):
               temp["sensor"].append( { self.sensores[j] : { "value": row[j] } } )

            dataset.append(temp)

            if row == None:
               break
            i = i + 1
            if i == 10: break

         self.conn.close()
         return dataset
      
# databaseName = input("¿Que base de datos desea importar? ")
databaseName = "Estacion26"
u = uploader(databaseName)

# TODO: Remove
temp = input("Presione ctrl + c  para terminar")

data = u.loadSQL()
print(data)