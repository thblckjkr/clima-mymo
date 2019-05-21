# simple information importer
import json
import MySQLdb
import requests

# xml requests
from xml.dom import minidom

class uploader:
   def __init__(self):
      # Get xml from uri
      r = requests.get(config['schema']['url'], allow_redirects=False)
      xmldoc = minidom.parse(r.content)
      itemlist = xmldoc.getElementsByTagName('Estacion')
      print(itemlist)


with open('../config/config.json') as json_file:
   config = json.load(json_file)

conn = MySQLdb.connect(
   host = config['mysql']['host'],
   user = config['mysql']['username'],
   passwd = config['mysql']['username']
)

u = uploader()

temp = raw_input("Que base de datos desea importar?")

cursor = conn.cursor()
cursos.execute('use ' + database)
cursor.execute('select * from archive')



# Obtener una a una toda la informacion
while True:
   row = cursor.fetchone()
   if row == None:
      break
   print(row)

db.close()