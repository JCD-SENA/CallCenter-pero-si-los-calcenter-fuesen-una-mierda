import json
import csv
import os
import webbrowser
import datetime

from modulos.softphone import *
from modulos.AgenteHandle import *
from modulos.clienteHandle import *
from modulos.notasHandle import *

class cliente:
	def __init__(self):
		self.loggeado = False
		self.phone = softphone("softphone\microSIP-agente")
		self.leerFecha = datetime.datetime
		self.ah = agenteHandle(self)
		self.ch = clienteHandle(self)
		self.nh = notasHandle(self)
	
	def main(self):
		os.system("cls")
		while True:
			if not self.loggeado:
				self.nombre = input("Ingrese el nombre de usuario: ")
				self.password = input("Ingrese la contraseña: ")
				self.data = self.logeoVerificar(self.nombre, self.password)
				self.activo = True
				if self.data:
					print("--------------------------------------")
					print("Se a ingresado la sesión exitosamente!\nIngresa 0 para ver los comandos")	
					print("--------------------------------------")				
					self.loggeado = True
					self.admin = self.data["tipo usuario"] == "0"
					self.permiso1 = self.data["permiso1"] == "TRUE"
					self.permiso2 = self.data["permiso2"] == "TRUE"
					self.descansoForzado = self.data["descanso forzado"] == "1"
					self.hacerRegistro(1, self.data["id"])
				else:
					print("Datos equivocados")
			else:
				opt = input("> ")
				descansoInicio = self.leerFecha.strptime(self.data["descanso inicio"], "%H:%M")
				descansoFin = self.leerFecha.strptime(self.data["descanso final"], "%H:%M")
				horaActual = self.leerFecha.strptime(self.leerFecha.today().strftime("%H:%M"), "%H:%M")
				#print(descansoInicio, descansoFin, horaActual)
				if self.descansoForzado:
					self.activo = False
				else:
					if descansoInicio < descansoFin:
						if horaActual >= descansoInicio and horaActual <= descansoFin:
							self.activo = False
							self.hacerRegistro(3, self.data["id"])
						else:
							if self.activo == False:
								self.hacerRegistro(2, self.data["id"])
							self.activo = True
					else:
						if horaActual >= descansoInicio or horaActual <= descansoFin:
							self.activo = False
							self.hacerRegistro(3, self.data["id"])
						else:
							if self.activo == False:
								self.hacerRegistro(2, self.data["id"])
							self.activo = True

				comandos = "\n1. Llamar cliente\n2. Registrar cliente\n3. Consultar clientes\n4. Realizar nota\n5. Cerrar sesión\n6. Cerrar programa\n"
				if self.data["permiso1"] == "TRUE":
					if self.activo:
						comandos+="7. Descansar\n"
					else:
						comandos+="7. Terminar descanso\n"
				if self.admin:
					comandos+="8. Ver grabaciones\n9. Gestionar agentes\n10. Ver registros\n"
				if opt == "0":
					print(comandos)
				if self.activo:
					if opt == "1":
						self.ch.llamarCliente()
					elif opt == "2":
						self.ch.registrarCliente()
					elif opt == "3":
						self.ch.consultarClientes()
					elif opt == "4":
						self.nh.crearNota()
				elif not self.activo and opt in ("1", "2", "3", "4", "5", "6"):
					print("Se deshabilitan los comandos hasta que termine el descanso")
				if opt == "6":
					self.cerrarSesion()
					print("Termiando ejecución")
					break
				elif opt == "5":
					self.cerrarSesion()
				elif opt == "7" and self.permiso1:
					self.descanso()
				if self.admin:
					if opt == "8":
						self.verGrabaciones()
					if opt == "9":
						self.ah.gestionarAgentes()
					if opt == "10":
						self.verRegistros()

	def verRegistros(self):
		registros = []
		for l in self.listar("logs"):
			registros.append([l[0], int(l[1]), l[2], l[3], l[4]])
		self.mostrarRegistros(registros)

	def verRegistrosCliente(self, client):
		registros = []
		for l in self.listar("logs"):
			if client == l[2]:
				registros.append([l[0], int(l[1]), l[2], l[3], l[4]])
		self.mostrarRegistros(registros)
	
	def verRegistrosAgente(self, agente):
		registros = []
		for l in self.listar("logs"):
			if agente == l[3]:
				registros.append([l[0], int(l[1]), l[2], l[3], l[4]])
		self.mostrarRegistros(registros)

	def mostrarRegistros(self, registros):
		print("\nID |Fecha           |Contenido")
		for r in registros:
			print(r[0]+(" "*(3 - len(r[0])))+"|"+r[4]+"|",end="")
			tipo = r[1]
			agente = None
			cliente = None
			if r[2] != "-1":
				cliente = self.ch.encontrarCliente(r[2])[1]
			if r[3] != "-1":
				agente = self.ah.encontrarAgente(r[3])[1]
			if tipo == 1:
				print(agente,"ha iniciado sesión")
			elif tipo == 2:
				print("Inicia el descanso de",agente)
			elif tipo == 3:
				print("Termina el descanso de",agente)
			elif tipo == 4:
				if cliente:
					print(agente,"realiza una llamada a",cliente)
				else:
					print(agente,"realiza una llamada")
			elif tipo == 5:
				print("Se ha actualizado al agente",agente)
			elif tipo == 6:
				print(agente,"ha registrado el cliente",r[3])
			elif tipo == 7:
				print(agente,"ha creado una nota",r[3])
			elif tipo == 8:
				print(agente,"ha creado el agente",r[3])
			elif tipo == 9:
				print(agente,"ha cerrado sesión")
			elif tipo == 10:
				print(agente,"ha cambiado los permisos del agente",r[3])
			elif tipo == 12:
				print(agente,"ha borrado la nota",r[3])
			elif tipo == 13:
				print(agente,"ha borrado al cliente",r[3])
			elif tipo == 14:
				print(agente,"ha borrado al agente",r[3])
			elif tipo == 15:
				print(agente, "ha actualizado los datos de",cliente)
			else:
				print("")
		print("")

	def hacerRegistro(self, tipo, agenteId=-1, clienteId=-1):
		logsArchivo = open("data/logs.csv", "a", newline='', encoding='utf-8')
		sobreescritor = csv.writer(logsArchivo)
		id=0
		for c in self.listar("logs"):
			id = int(c[0])
		fecha = self.leerFecha.today().strftime("%d/%m/%Y %H:%M")
		sobreescritor.writerow([id+1, tipo, clienteId, agenteId, fecha])

	def verGrabaciones(self, verMenu=True):
		dirGrab = "./data/grabaciones"
		grabaciones = os.listdir(dirGrab)
		cont = "\n.-------------------------------------------------------------.\n"
		cont +=  "|Num |Fecha           |Numero cliente |Numero agente |Tipo    |\n"
		cont +=  "|-------------------------------------------------------------|\n"
		num = 0
		for g in grabaciones:
			partsFile = g.split("-")
			year = partsFile[0][0:4]
			month = partsFile[0][4:6]
			day = partsFile[0][6:8]

			hora = partsFile[1][0:2]
			minutos = partsFile[1][2:4]

			numeroA = partsFile[2]
			numeroB = partsFile[4][:-4]

			num += 1

			tipo = "Entrada" if partsFile[3] == "incoming" else "Salida"
			cont += "|"+str(num)+(" "*(4 - len(str(num))))+"|"+day+"/"+month+"/"+year+" "+hora+":"+minutos+"|"+numeroA+(" "*(15 - len(numeroA)))+"|"+numeroB+(" "*(14 - len(numeroB)))+"|"+tipo+(" "*(8-len(tipo)))+"|\n"
		cont += "°-------------------------------------------------------------°"
		print(cont)
		if verMenu:
			while True:
				print("1. Escuchar grabación\n2. Salir\n")
				opt2 = input("> ")
				if opt2 == "1":
					sNum = int(input("Ingrese el número de la grabación: ")) - 1
					print("Abriendo grabación...\n")
					webbrowser.open("file:\\\\"+os.getcwd()+dirGrab[1:]+"\\"+grabaciones[sNum],new=2)
				else:
					print("Saliendo al menú principal")
					break

	def descanso(self):
		if self.activo:
			print("Iniciando descanso")
			self.descansoForzado = True
			self.hacerRegistro(2, self.data["id"])
		else:
			print("Terminando descanso")
			self.descansoForzado = False
			self.hacerRegistro(3, self.data["id"])
		self.activo = not self.activo
		cont = "id,nombre,numero,permiso1,permiso2,pass,descansoStart,descansoEnd,tipo,activo\n"
		for ag in self.listar("agentes"):
			if ag[0] == self.data["id"]:
				cont += ag[0]+","+ag[1]+","+ag[2]+","+ag[3]+","+ag[4]+","+ag[5]+","+ag[6]+","+ag[7]+","+ag[8]+","+("0" if self.activo else "1")+"\n"
			else:
				cont += ag[0]+","+ag[1]+","+ag[2]+","+ag[3]+","+ag[4]+","+ag[5]+","+ag[6]+","+ag[7]+","+ag[8]+","+ag[9]+"\n"
		agentesArchivo = open("data/agentes.csv", "w")
		agentesArchivo.write(cont)
		agentesArchivo.close()

	def cerrarSesion(self):
		self.hacerRegistro(9, self.data["id"])
		self.data = None
		self.nombre = ""
		self.password = ""
		self.loggeado = False
	
	def logeoVerificar(self, nombre, password):
		agente = None
		for ag in self.listar("agentes"):
			if ag[1]==nombre and ag[5]==password:
				agente = {
					"id": ag[0],
					"nombre": ag[1],
					"numero": ag[2],
					"permiso1": ag[3],
					"permiso2": ag[4],
					"pass": ag[5],
					"descanso inicio": ag[6],
					"descanso final": ag[7],
					"tipo usuario": ag[8],
					"descanso forzado": ag[9]
				}
				break
		return agente
	
	def listar(self,archivo):
		listaArchivo = open("data/"+archivo+".csv", "r")
		lista=csv.reader(listaArchivo)
		return list(lista)[1:]

if __name__ == "__main__":
	c = cliente()
	c.main()