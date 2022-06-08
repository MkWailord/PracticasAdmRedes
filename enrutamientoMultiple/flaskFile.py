from flask import Flask
import enrutamientoMult

app = Flask(__name__)

@app.route('/')
def enrutamientoMultiple():
	return enrutamientoMult.enrutMult("admin","admin")
	
	
if __name__=='__main__':
	app.run(host='0.0.0.0', debug = True)
