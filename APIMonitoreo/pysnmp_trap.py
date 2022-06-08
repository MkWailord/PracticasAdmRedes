from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import logging
import os

snmpEngine = engine.SnmpEngine()
TrapAgentAddress = '192.168.1.2'
Port = 162;

logging.basicConfig(filename='traps_recibidas.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

#print("Escuchando trampas en "+TrapAgentAddress+": "+str(Port))

config.addTransport(
	snmpEngine,
	udp.domainName + (1,),
	udp.UdpTransport().openServerMode((TrapAgentAddress,Port))
)

config.addV1System(snmpEngine, 'todo', 'secreta')

def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
	print("Mensaje nuevo de traps recibido");
	logging.info("Mensaje nuevo de traps recibido")
	for name, val in varBinds:
		logging.info(f"{name.prettyPrint()} = {val.prettyPrint()}")
		print(f"{name.prettyPrint()} = {val.prettyPrint()}")
	logging.info("==== Fin del mensaje de la trampa ====")

ntfrcv.NotificationReceiver(snmpEngine, cbFun)
snmpEngine.transportDispatcher.jobStarted(1)

def getIntStatus():
	int_status = []
	if os.path.isfile("traps_recibidas.log"):
		with open("traps_recibidas.log") as traps:
			all_lines = traps.readlines()
			int_status = list(filter(lambda x: x.find("1.3.6.1.4.1.9.2.2.1.1.20.1") != -1, all_lines))
	else:
		return None

	return int_status

def runTrap():
	try:
		snmpEngine.transportDispatcher.runDispatcher()
	except Exception as ex:
		print(ex)
		logging.info(ex)
		snmpEngine.transportDispatcher.closeDispatcher()
		raise

if __name__ == "__main__":
	logging.info("Escuchando trampas en "+TrapAgentAddress+": "+str(Port))
	logging.info("######################################################")
	run()
