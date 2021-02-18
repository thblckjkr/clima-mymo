class UI:
	colors = {
		'header' : '\033[95m', 'info' : '\033[94m', 'success' : '\033[92m', 'warning' : '\033[93m',
		'error' : '\033[91m', 'ENDC' : '\033[0m', 'bold' : '\033[1m', 'underline' : '\033[4m'
	}
	def __init__(self):
		self.show("Inicializando interfaz...\n", 'info')
		
	def show(self, message, type = 'info'):
		color = self.colors.get(type, "Invalid color")
		print (color + message + self.colors['ENDC'])

	def askYesNo(self, message):
		self.show(message, 'info')
		message = "Presiona: \n [0] para NO\n [1] para SI\n Tu respuesta: "
		while(True):
			temp = input(message)
			if temp != '0' and temp != '1':
				self.show("No has seleccionado un valor coherente", 'warning')
			else:
				return int(temp)

	def askNumber(self, message, t ='int'):
		self.show(message, 'info')
		message = ""
		while(True):
			temp = input("")
			try:
				if t == 'float':
					xtemp = float(temp)
				else:
					xtemp = int(temp)
				
				return xtemp
			except ValueError:
				self.show("No has seleccionado un valor coherente", 'warning')

	def ask(self, message):
		self.show(message, 'info')
		message = ""
		temp = input("")
		return temp