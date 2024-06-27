import subprocess

from modulos.configuracion import *

class softphone:
	def __init__(self, path):
		self.ejecutable = path
	
	def llamar(self, data):
		c = configuracion(self.ejecutable+"\\microsip.ini", data)
		c.reescribir()
		subprocess.run([".\\"+self.ejecutable+"\\microsip.exe"])