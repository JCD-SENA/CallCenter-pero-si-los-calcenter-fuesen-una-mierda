import csv

class notasHandle:
	def __init__(self, admin):
		self.admin = admin
	
	def crearNota(self):
		num = input("Ingrese el número del cliente: ")
		client = None
		for c in self.admin.listar("clientes"):
			if c[2] == num:
				client = c
		if client:
			cont = "\""+input("Escriba el contenido de la nota:\n")+"\""
			notasArchivo = open("data/notas.csv", "a", newline='', encoding='utf-8')
			sobreescritor = csv.writer(notasArchivo)
			id=0
			for c in self.admin.listar("notas"):
				id = int(c[0])
			fecha = self.admin.leerFecha.today().strftime("%d/%m/%Y %H:%M")
			sobreescritor.writerow([id+1, client[0], cont, fecha, self.admin.data["id"]])
			self.admin.hacerRegistro(7, self.admin.data["id"], id+1)
			print("Nota creada")
		else:
			print("No se pueden realizar notas sobre un cliente no registrado")

	def verNotas(self, id=None, verMenu=True):
		clientes = []
		if id:
			cliente = None
			for c in self.admin.listar("clientes"):
				if c[0] == id:
					cliente = c
			if cliente:
				clientes.append(cliente)
				print("\nNotas de "+cliente[1])
			else:
				print("Cliente no encontrado")
				return None
		else:
			clientes = self.admin.listar("clientes")
		print(".---------------------------------------------------------------------------------------------.")
		print("|id |Cliente         |Agente         |fecha           |Nota                                   |")
		print("-----------------------------------------------------------------------------------------------")
		for n in self.admin.listar("notas"):
			cliente = None
			agente = None
			for c in clientes:
				if c[0] == n[1]:
					cliente = c
					break
			for a in self.admin.listar("agentes"):
				if a[0] == n[4]:
					agente = a
					break
			if cliente and agente:
				linea = "|"+n[0]+(" " * (3-(len(c[0]))))+"|"+cliente[1]+(" " * (16 - len(cliente[1])))+"|"+agente[1]+(" "*(15 - len(agente[1])))+"|"+n[3]+"|"
				lineas = int(len(n[2]) / 39)
				for _ in range(0, lineas + 1):
					nLinea = n[2][(39 * _):(39 * (_ + 1))]
					if _ == 0:
						linea+=nLinea+(" " * (39 - len(nLinea)))+"|"
					else:
						linea+="\n|   |                |               |                |"+nLinea+(" " * (39 - len(nLinea)))+"|"
				print(linea)
				print("-----------------------------------------------------------------------------------------------")
		print("")
		if self.admin.permiso2 and verMenu:
			print("1. Ver notas\n2. Borrar nota\n3. Salir\n")
			while True:
				opt3 = input("> ")
				if opt3 == "1":
					self.verNotas(id, False)
				elif opt3 == "2":
					notaId = input("Ingrese el ID de la nota:")
					self.borrarNota(notaId)
				elif opt3=="3":
					print("Saliendo al sub-menú")
					break
	
	def borrarNota(self, notaId):
		cont = "id,cliente,contenido,fecha,agente\n"
		for n in self.admin.listar("notas"):
			if n[0] != notaId:
				cont += n[0]+","+n[1]+",\""+n[2]+"\","+n[3]+","+n[4]+"\n"
		notasArchivo = open("data/notas.csv", "w")
		notasArchivo.write(cont)
		notasArchivo.close()
		self.admin.hacerRegistro(12, self.admin.data["id"], notaId)
		print("Nota "+notaId+" fue borrada")