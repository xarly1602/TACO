from simplecrypt import encrypt, decrypt
from binascii import hexlify, unhexlify

class Utilidades():

	def encriptar(self, cont, msje):
		encriptado = encrypt(cont, msje)
		link = hexlify(encriptado)
		return link

	def desencriptar(self, cont, msje):
		desencriptar = unhexlify(msje)
		uid = decrypt(cont, desencriptar)
		return uid

	def esquemaSemanal(self, dosisSemana):
		contador = 0;
		esquema = ["","","","","","",""]
		dosisSemana = int(dosisSemana)
		dosisDia= dosisSemana/7
		resto = dosisSemana%7
		while contador < len(esquema):		
			esquema[contador] = str(dosisDia)
			contador = contador+1
		if resto == 1:
			esquema[0] = str(int(esquema[0])+1) + "/4"
			esquema[1] = esquema[1] + "/4"
			esquema[2] = esquema[2] + "/4"
			esquema[3] = esquema[3] + "/4"
			esquema[4] = esquema[4] + "/4"
			esquema[5] = esquema[5] + "/4"
			esquema[6] = esquema[6] + "/4"
		elif resto == 2:
			esquema[0] = str(int(esquema[0])+1) + "/4"
			esquema[3] = str(int(esquema[3])+1) + "/4"
			esquema[1] = esquema[1] + "/4"
			esquema[2] = esquema[2] + "/4"
			esquema[4] = esquema[4] + "/4"
			esquema[5] = esquema[5] + "/4"
			esquema[6] = esquema[6] + "/4"
		elif resto == 3:
			esquema[0] = str(int(esquema[0])+1) + "/4"
			esquema[5] = str(int(esquema[5])+1) + "/4"
			esquema[2] = str(int(esquema[2])+1) + "/4"
			esquema[1] = esquema[1] + "/4"
			esquema[3] = esquema[3] + "/4"
			esquema[4] = esquema[4] + "/4"
			esquema[6] = esquema[6] + "/4"
		elif resto == 4:
			esquema[0] = str(int(esquema[0])+1) + "/4"
			esquema[3] = str(int(esquema[3])+1) + "/4"
			esquema[1] = str(int(esquema[1])+1) + "/4"
			esquema[5] = str(int(esquema[5])+1) + "/4"
			esquema[2] = esquema[2] + "/4"
			esquema[4] = esquema[4] + "/4"
			esquema[6] = esquema[6] + "/4"
		elif resto == 5:
			esquema[0] = str(int(esquema[0])+1) + "/4"
			esquema[4] = str(int(esquema[4])+1) + "/4"
			esquema[2] = str(int(esquema[2])+1) + "/4"
			esquema[5] = str(int(esquema[5])+1) + "/4"
			esquema[1] = str(int(esquema[1])+1) + "/4"
			esquema[3] = esquema[3] + "/4"
			esquema[6] = esquema[6] + "/4"
		elif resto == 6:
			esquema[0] = str(int(esquema[0])+1) + "/4"
			esquema[4] = str(int(esquema[4])+1) + "/4"
			esquema[2] = str(int(esquema[2])+1) + "/4"
			esquema[3] = str(int(esquema[3])+1) + "/4"
			esquema[1] = str(int(esquema[1])+1) + "/4"
			esquema[5] = str(int(esquema[5])+1) + "/4"
			esquema[6] = esquema[6] + "/4"
		else:
			esquema[0] = esquema[0] + "/4"
			esquema[1] = esquema[1] + "/4"
			esquema[2] = esquema[2] + "/4"
			esquema[3] = esquema[3] + "/4"
			esquema[4] = esquema[4] + "/4"
			esquema[5] = esquema[5] + "/4"
			esquema[6] = esquema[6] + "/4"		
			
		return esquema