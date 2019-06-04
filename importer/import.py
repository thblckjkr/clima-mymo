# Simple information importer
# This one is dirty AF [@thblckjkr]

import json
import pymysql
import requests

# xml requests
from xml.dom import minidom

# Import configuration
with open('../config/config.json') as json_file:
   config = json.load(json_file)

class uploader:

   def __init__(self, db):
      # Get a database and load the corresponding everything from the public XML
      self.loadXML(db)

   def loadXML(self, db):
      r = requests.get(config['schema']['url'], allow_redirects = False)
      xmldoc = minidom.parseString(r.content)
      itemlist = xmldoc.getElementsByTagName('Estacion')

      for item in itemlist:
         estacion =  item.getElementsByTagName('nombre')[0]
         for dato in estacion.childNodes:
            temp = dato.data.split(" ")
            temp = "".join(temp)
            if temp == db:
               

#databaseName = input("¿Que base de datos desea importar?")
databaseName = "Estacion09"
u = uploader(databaseName)

# TODO: Remove
temp = input("Presione ctrl + c  para terminar")


conn = pymysql.connect(
   host = config['mysql']['host'],
   user = config['mysql']['username'],
   passwd = config['mysql']['password']
)

cursor = conn.cursor()
cursor.execute('use ' + database)
cursor.execute('select * from archive')


# Obtener una a una toda la informacion
while True:
   row = cursor.fetchone()
   if row == None:
      break
   print(row)

db.close()