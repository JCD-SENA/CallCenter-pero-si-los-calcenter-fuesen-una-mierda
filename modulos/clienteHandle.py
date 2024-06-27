import csv

class clienteHandle:
	def __init__(self, admin):
		self.admin = admin

	def llamarCliente(self, client=None):
		print("Abriendo el telefono")
		if client:
			self.admin.hacerRegistro(4, self.admin.data["id"], client)
		else:
			self.admin.hacerRegistro(4, self.admin.data["id"])
		self.admin.phone.llamar(self.admin.data)
		print("Cerrando")

	def menuCliente(self):
		print("1. Llamar cliente\n2. Ver notas\n3. Salir\n")
		if self.admin.admin:
			print("4. Ver actividad\n5. Eliminar usuario\n6. Editar usuario\n")

	def verClientes(self):
		cs = []
		ln = 0
		nn = 0
		for c in self.admin.listar("clientes"):
			cs.append(c)
			if len(c[1]) > ln:
				ln = len(c[1]) - len("Nombre")
			if len(c[2]) > nn:
				nn = len(c[2]) - len("Numero")
		print("\n.-----------------"+("-" * (ln + nn))+".")
		print("|ID |Nombre"+(" "*ln)+"|Numero"+(" "*nn)+"|")
		print("-------------------"+("-" * (ln + nn)))
		for c in cs:
			print("|"+c[0]+(" " * (3-len(c[0])))+"|"+c[1]+(" " * (6 - len(c[1])))+"|"+c[2]+(" " * (6 - len(c[2])))+"|")
		print("°-----------------"+("-" * (ln + nn))+"°\n")
		self.menuCliente()

	def consultarClientes(self):
		self.verClientes()
		while True:
			opt2 = input("> ")
			if opt2 in ("1", "2"):
				num = input("Ingrese el id del usuario: ")
			if opt2 == "1":
				num = input("Ingrese el id del usuario: ")
				self.llamarCliente(num)
			elif opt2 == "2":
				self.admin.nh.verNotas(num)
			elif opt2 == "3":
				print("Regresando al menú principal")
				break
			if self.admin and opt2 in ("4", "5", "6"):
				num = input("Ingrese el id del usuario: ")
				if opt2 == "4":
					self.admin.verRegistrosCliente(num)
				elif opt2 == "5":
					self.borrarCliente(num)
				elif opt2 == "6":
					self.editarCliente(num)

	def editarCliente(self, id):
		nombre = None
		numero = None
		client = self.encontrarCliente(id)
		if client:
			nombre = client[1]
			numero = client[2]
			print("\n.---------------------------------------.")
			print("|Nombre                   |Numero       |")
			print("|---------------------------------------|")
			print("|"+nombre+(" "* (25 - len(nombre)))+"|"+numero+(" "* (13 - len(numero)))+"|")
			print("°---------------------------------------°\n\n(Para no sobreescribir cada dato solo preciona enter)\n")

			nNombre = input("Ingrese el nuevo nombre: ")
			nNumero = input("Ingrese el nuevo número: ")
			if not nNombre:
				nNombre = nombre
			if not nNumero:
				nNumero = numero

			cont = "id,nombre,numero,estado\n"
			for c in self.admin.listar("clientes"):
				if c[0] != id:
					cont += c[0]+","+c[1]+","+c[2]+","+c[3]+"\n"
				else:
					cont += c[0]+","+nNombre+","+nNumero+","+c[3]+"\n"
			clienteArchivo = open("data/clientes.csv", "w")
			clienteArchivo.write(cont)
			clienteArchivo.close()
			self.admin.hacerRegistro(15, self.admin.data["id"], id)
			print("Cliente editado")
			self.verClientes()
		else:
			print("No se pudo encontar el cliente")

	def borrarCliente(self, clienteId):
		for n in self.admin.listar("notas"):
			if n[1] == clienteId:
				self.admin.nh.borrarNota(n[0])
		cont = "id,nombre,numero,estado\n"
		for c in self.admin.listar("clientes"):
			if c[0] != clienteId:
				cont += c[0]+","+c[1]+",\""+c[2]+"\","+c[3]+"\n"
		clienteArchivo = open("data/clientes.csv", "w")
		clienteArchivo.write(cont)
		clienteArchivo.close()
		self.admin.hacerRegistro(13, self.admin.data["id"], clienteId)
		print("Cliente "+clienteId+" fue borrado")
	
	def registrarCliente(self):
		clienteLista = open("data/clientes.csv", "a", newline='', encoding='utf-8')
		sobreescritor = csv.writer(clienteLista)
		nombre=input("Ingrese el nombre del cliente: ")
		numero=input("Ingrese el número del cliente: ")
		id=0
		for c in self.admin.listar("clientes"):
			id = int(c[0])
		sobreescritor.writerow([id+1, nombre, numero, "1"])
		self.admin.hacerRegistro(6, self.admin.data["id"], id+1)
		print("Cliente registrado")

	def encontrarCliente(self, id):
		client = None
		for c in self.admin.listar("clientes"):
			if c[0] == id:
				client = c
				break
		return client