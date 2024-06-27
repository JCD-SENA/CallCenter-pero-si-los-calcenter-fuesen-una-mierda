class configuracion:
	def __init__(self, iniPath, data):
		self.iniArchivo = open(iniPath, "r+", encoding="utf16")
		self.ini = self.iniArchivo.readlines()
		self.cuentaPos = self.ini.index("[Account1]\n")
		self.labelPos = self.cuentaPos + 1
		self.usernamePos = self.cuentaPos + 5
		self.displayNamePos = self.cuentaPos + 8
		self.nombre = data["numero"]
		self.nombreDisplay = data["nombre"]
		self.secret = data["pass"]

	def reescribir(self):
		cont = ""
		for _ in range(len(self.ini)):
			if not _ in [self.labelPos, self.usernamePos, self.displayNamePos]:
				cont += self.ini[_]
			else:
				if _ == self.labelPos:
					cont += "label="+self.nombre+"\n"
				if _ == self.usernamePos:
					cont += "username="+self.nombre+"\n"
				if _ == self.displayNamePos:
					cont += "displayName="+self.nombreDisplay+"\n"
		self.iniArchivo.seek(0)
		self.iniArchivo.write(cont)
		self.iniArchivo.truncate()