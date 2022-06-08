import os
from threading import Thread
from time import sleep
from pysnmp.entity.rfc3413.oneliner import cmdgen

from pysnmp_trap import runTrap, getIntStatus

cmdGen = cmdgen.CommandGenerator()
community = "secreta"
host = "192.168.1.1"
puerto = 161
interfaceOID = "1.3.6.1.2.1.2.2.1.10.1"
def snmpQuery(oid):
	errorInd, errorStat, errorIdx, varBinds = cmdGen.getCmd(cmdgen.CommunityData(community),
							cmdgen.UdpTransportTarget((host,puerto)),
							oid)
	if errorInd:
		print(errorInd)
	else:
		if errorStat:
			print(f"Error:{errorStat.prettyPrint()} en {errorIdx and varBinds[int(errorIdx)-1] or '?'}")
		else:
			for _, val in varBinds:
				return str(val)

delay = 5
valorInicial = 0
valorUltimo = 0

if __name__ == "__main__":
	print("Escuchando trampas en: "+host+": " +str(puerto))
	Thread(target=runTrap).start()

	if os.path.isfile("monitor.log"):
		os.remove("monitor.log")
	while(True):
		print("*******REALIZANDO CONSULTA******")
		datos = int(snmpQuery(interfaceOID))
		datos = int(datos/98) - valorInicial
		with open("monitor.log", "a+") as f:
			intStatus = getIntStatus()
			status = [x.split(" = ")[1].replace("\n", "") for x in intStatus]
			if len(status) > 0:
				ultimoStatus = status[len(status)-1]
				if ultimoStatus != "up":
					f.write(f"{None}\n")
					sleep(delay)
					continue
			f.seek(0)
			lineas = f.readlines()[::-1]
			if len(lineas) == 0:
				f.seek(0,2)
				valorInicial = datos
				f.write(f"{0}\n")
			else:
				f.seek(0,2)
				imprimir = datos - valorUltimo
				valorUltimo += imprimir
				f.write(f"{imprimir}\n")

		sleep(delay)
