from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Crea una aplicación Flask, carga la configuración
# y crea el objeto SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miRed.db'
bd = SQLAlchemy(app)

# This is the database model object
class Dispositivo(bd.Model):
    __tablename__ = 'dispositivos'
    id = bd.Column(bd.Integer, primary_key=True)
    hostname = bd.Column(bd.String(120), index=True)
    empresa = bd.Column(bd.String(40))

    def __init__(self, hostname, empresa):
        self.hostname = hostname
        self.empresa = empresa

    def __repr__(self):
        return '<Dispositivo %r>' % self.hostname


if __name__ == '__main__':
    bd.create_all()
    R1 = Dispositivo('lax-dc1-core1', 'Juniper')
    R2 = Dispositivo('sfo-dc1-core1', 'Cisco')
    bd.session.add(R1)
    bd.session.add(R2)
    bd.session.commit()

