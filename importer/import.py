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
      self.loadXML(db)

   def loadXML(self, db):
      r = requests.get(config['schema']['url'], allow_redirects = False)
      xmldoc = minidom.parseString(r.content)
      itemlist = xmldoc.getElementsByTagName('Estacion')

      for item in itemlist:
         estacion =  item.getElementsByTagName('nombre')[0]
         for dato in estacion.childNodes:
            # temp = dato.data.split(" ")
            print (dato.data)
               

databaseName = input("¿Que base de datos desea importar?")
u = uploader(databaseName)

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