import csv

class agenteHandle:
	def __init__(self, admin):
		self.admin = admin
	
	def registrarAgente(self):
		nombre = input("Ingrese el nombre del nuevo agente: ")
		numero = input("Ingrese el numero del nuevo agente: ")
		contra = input("Ingrese la contraseña del agente: ")
		desIni = input("Ingrese el inicio del descanso (HH:MM) del nuevo agente: ")
		desFin = input("Ingrese el final del descanso (HH:MM) del nuevo agente: ")
		agenteLista = open("data/agentes.csv", "a", newline='', encoding='utf-8')
		sobreescritor = csv.writer(agenteLista)
		id=0
		for c in self.admin.listar("agentes"):
			id = int(c[0])
		sobreescritor.writerow([id+1, nombre, numero, "FALSE", "FALSE", contra, desIni, desFin, "1", "0"])
		self.admin.hacerRegistro(8, self.admin.data["id"], id+1)
		print("Agente registrado")

	def borrarAgente(self):
		agenteId = input("Ingrese el id del agente: ")
		cont = "id,nombre,numero,permiso1,permiso2,pass,descansoStart,descansoEnd,tipo,activo\n"
		for a in self.admin.listar("agentes"):
			if a[0] != agenteId:
				cont += a[0]+","+a[1]+","+a[2]+","+a[3]+","+a[4]+","+a[5]+","+a[6]+","+a[7]+","+a[8]+","+a[9]+"\n"
		clienteArchivo = open("data/agentes.csv", "w")
		clienteArchivo.write(cont)
		clienteArchivo.close()
		self.admin.hacerRegistro(14, self.admin.data["id"], agenteId)
		print("Agente "+agenteId+" fue borrado")

	def cambiarPermisos(self):
		agenteId = input("Ingrese el ID del agente: ")
		agente = self.encontrarAgente(agenteId)
		if agente:
			print("\nPermisos del agente "+agente[1])
			print("[Declarar descansos|"+("Si" if agente[3] == "TRUE" else "No")+"]")
			print("[Borrar notas      |"+("Si" if agente[4] == "TRUE" else "No")+"]\n")
			cont = "id,nombre,numero,permiso1,permiso2,pass,descansoStart,descansoEnd,tipo,activo\n"
			for a in self.admin.listar("agentes"):
				if a[0] != agenteId:
					cont += a[0]+","+a[1]+","+a[2]+","+a[3]+","+a[4]+","+a[5]+","+a[6]+","+a[7]+","+a[8]+","+a[9]+"\n"
				else:
					p1 = input("Declarar descansos (S/N): ")
					p2 = input("Borrar notas (S/N): ")
					cont += agente[0]+","+agente[1]+","+agente[2]+","+("TRUE" if p1 == "s" else "FALSE")+","+("TRUE" if p2 == "s" else "FALSE")+","+agente[5]+","+agente[6]+","+agente[7]+","+agente[8]+","+agente[9]+"\n"
			clienteArchivo = open("data/agentes.csv", "w")
			clienteArchivo.write(cont)
			clienteArchivo.close()
			self.admin.hacerRegistro(10, self.admin.data["id"], agenteId)
			print("Permisos cambiados")
		else:
			print("Agente no encontrado")

	def agentesMenu(self):
		print("1. Añadir agentes\n2. Cambiar permisos\n3. Editar agentes\n4. Eliminar clientes\n5. Ver actividad\n\n6. Salir\n")

	def gestionarAgentes(self):
		self.verAgentes()
		self.agentesMenu()
		while True:
			opt2 = input("> ")
			if opt2 == "1":
				self.registrarAgente()
				self.verAgentes()
			elif opt2 == "2":
				self.cambiarPermisos()
				self.verAgentes()
			elif opt2 == "3":
				self.editarAgente()
				self.verAgentes()
			elif opt2 == "4":
				self.borrarAgente()
				self.verAgentes()
			elif opt2 == "5":
				num = input("Ingrese el id del agente: ")
				self.admin.verRegistrosAgente(num)
			elif opt2 == "6":
				print("Regresando al menú principal")
				break
			elif opt2 == "0":
				self.agentesMenu()

	def editarAgente(self):
		agenteId = input("Ingrese el id del agente: ")
		agente = self.encontrarAgente(agenteId)
		if agente:
			cont = "id,nombre,numero,permiso1,permiso2,pass,descansoStart,descansoEnd,tipo,activo\n"
			for a in self.admin.listar("agentes"):
				if agenteId != a[0]:
					cont += a[0]+","+a[1]+","+a[2]+","+a[3]+","+a[4]+","+a[5]+","+a[6]+","+a[7]+","+a[8]+","+a[9]+"\n"
				else:
					print("\n(Para no sobreescribir cada dato solo preciona enter)\n")
					nNombre = input("Ingrese el nuevo nombre: ")
					nNumero = input("Ingrese el nuevo numero: ")
					nPass = input("Ingrese la nueva contraseña: ")
					nDesEs = input("Ingrese el inicio del descanso (HH:MM): ")
					nDesFi = input("Ingrese el nuevo final del descano (HH:MM): ")
					if not nNombre:
						nNombre = a[1]
					if not nNumero:
						nNumero = a[2]
					if not nPass:
						nPass = a[5]
					if not nDesEs:
						nDesEs = a[6]
					if not nDesFi:
						nDesFi = a[7]
					cont += a[0]+","+nNombre+","+nNumero+","+a[3]+","+a[4]+","+nPass+","+nDesEs+","+nDesFi+","+a[8]+","+a[9]+"\n"
			clienteArchivo = open("data/agentes.csv", "w")
			clienteArchivo.write(cont)
			clienteArchivo.close()
			self.admin.hacerRegistro(5, agenteId)
			print("Agente editado")
		else:
			print("No se pudo encontrar el agente")

	def verAgentes(self):
		print("\n.-------------------------------------------------------------------------------------------------------------------------------------------------.")
		print("|ID |Nombre         |Numero         |Contraseña     |Puede declarar sus propios descansos|Puede borrar notas|Descanso inicio|Descanso final|Activo|")
		print("|-------------------------------------------------------------------------------------------------------------------------------------------------|")
		for a in self.admin.listar("agentes"):
			if a[8] != "0":
				print(
					"|"+a[0]+(" "*(3 - len(str(a[0]))))+
					"|"+a[1]+(" "*(15 - len(a[1])))+
					"|"+a[2]+(" "*(15 - len(a[2])))+
					"|"+a[5]+(" " * (15 - len(a[5])))+
					"|"+("Si" if a[3] == "TRUE" else "No")+"                                  "+
					"|"+("Si" if a[4] == "TRUE" else "No")+"                "+
					"|"+a[6]+(" " * (15 - len(a[6])))+
					"|"+a[7]+(" " * (14 - len(a[7])))+
					"|"+("Si" if a[9] == "0" else "No")+"    |"
				)
		print("°-------------------------------------------------------------------------------------------------------------------------------------------------°\n")

	def encontrarAgente(self, id):
		agente = None
		for a in self.admin.listar("agentes"):
			if a[0] == id:
				agente = a
				break
		return agente