from flask import Flask, make_response, send_file
from pysnmp_trap import getIntStatus
import pygal
from pygal.style import Style
from pygal.style import LightSolarizedStyle
import os
app = Flask(__name__)

@app.get("/status")
def status():
	return make_response({"message": "Servidor Corriendo"},200)

@app.get("/interface/status")
def getInterfaceStatus():
	intStatus = getIntStatus()
	print(intStatus)
	if intStatus != None:
		if len(intStatus) == 0:
			return make_response({"error":"Sin cambios"}, 200)
		else:
			status = [x.split(" = ")[1].replace("\n","") for x in intStatus]
			return make_response({"message": "Estado de la interfaz Fa0/0",
			"status": status[len(status)-1], "Status":status},200)
	else:
		return make_response({"error": "Servicio no iniciado"}, 200)

@app.get("/interface/monitor")
def getInterfaceMonitor():
	if not os.path.isfile("monitor.log"):
		return make_response({"error": "Sin información"}, 200)

	paquetes = []
	intervalosDown = []

	with open("monitor.log", "r") as m:
		paquetes = [int(x) if x != "None\n" else None for x in m.readlines()]

	intervalos = []
	time = 0
	for _ in range (0, len(paquetes)):
		intervalos.append(time)
		time += 5

	for i in range(1, len(paquetes)-1, 1):
		if(paquetes[i] == None and type(paquetes[i-1]) == int):
			intervalosDown.append({"value": (intervalos[i], 0)})
			intervalosDown.append({"value": (intervalos[i], 0), "label": "Interfaz Caida"})
		if(type(paquetes[i])== int and paquetes[i-1] == None):
			intervalosDown.append({"value":(intervalos[i],0)})
			intervalosDown.append({"value":(intervalos[i],0)})
			intervalosDown.append({"value": None})
	estilo = Style(colors=('blue','red'))
	grafica = pygal.XY(show_x_guides = False, show_y_guides = True, range=(-2,10), print_labels = True, stroke = True, legend_at_bottom = True, style = LightSolarizedStyle)
	grafica.title = "Interfaz FastEthernet0/0"
	grafica.x_labels = intervalos
	grafica.add("Paquetes Recibidos", [(x,y) for x,y in zip(intervalos,paquetes)], allow_interruptions = True, stroke_color='blue')
	grafica.add("Interfaz Caida", intervalosDown, allow_interruptions = True)

	grafica.render_to_file("grafica.svg")

	return send_file("grafica.svg", mimetype="image/svg+xml")

if __name__ == "__main__":
	app.run("0.0.0.0",8000,True)
