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
      self.sensores = self.loadXML(db)
      self.db = db

      self.conn = pymysql.connect(
         host = config['mysql']['host'],
         user = config['mysql']['username'],
         passwd = config['mysql']['password']
      )

   def loadXML(self, db):
      r = requests.get(config['schema']['url'], allow_redirects = False)
      main = objectify.fromstring(r.content)

      for item in main.Estaciones.Estacion:
         if "".join(item.get("nombre").split(" ")) == db:
            print("Estacion encontrada, empezando a descargar")
            return item.sensores

   def loadSQL(self):
      fields = [ 'dateTime' ]
      for field in self.sensores.iterchildren():
         # Si hay datos que no sean iguales, ignorar
         if field.tag != field.sql:
            print ("Error raro, unhandled data")
            return
      
         fields.append( str( field.sql) )

      sql = " ,".join(fields)
      sql = 'select ' + sql + ' from archive order by dateTime desc'

      with self.conn.cursor() as cursor:
         cursor.execute('use ' + self.db)
         cursor.execute(sql)

         # Obtener una a una toda la informacion
         i = 0
         while True:
            row = cursor.fetchone()
            print(row)
            if row == None:
               break
            i = i + 1
            if i == 10: break

         self.conn.close()
      
#databaseName = input("¿Que base de datos desea importar?")
databaseName = "Estacion09"
u = uploader(databaseName)

# TODO: Remove
temp = input("Presione ctrl + c  para terminar")

u.loadSQL()