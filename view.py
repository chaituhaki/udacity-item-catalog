from flask import Flask, url_for, render_template, jsonify, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database_setup import Base, Services, ServiceItem, ServiceItemMenu

engine = create_engine("sqlite:///ItemCatalog.db")

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
app = Flask(__name__)

@app.route('/')
@app.route('/services/')
def showService():
    services = session.query(Services).all()
    return render_template('home.html', services = services)

#EDIT a Service
@app.route('/services/<int:service_id>/edit/', methods=['GET', 'POST'])
def serviceEdit(service_id):
    service = session.query(Services).filter_by(id=service_id).one()
    #POST request
    if request.method == 'POST':
        if request.form['name']:
            service.name = request.form['name']
            session.add(service)
            session.commit()
        return redirect(url_for('showService'))
    #GET request
    else:
        return render_template('editService.html', service = service)

#Add new Service
@app.route('/services/new', methods =['GET', 'POST'])
def serviceAddNew():
    if request.method == 'POST':
        if request.form['name']:
            service = Services(name = request.form['name'])
            session.add(service)
            session.commit()
            return redirect(url_for('showService'))
        else:
            alert = 'alert("Fill all required field")'
            return render_template('newService.html', alert= alert)
    else:
        return render_template('newService.html')

@app.route('/services/<int:service_id>/delete', methods=['GET', 'POST'])
def serviceDelete(service_id):
    service = session.query(Services).filter_by(id = service_id).one()
    if request.method == 'POST':
        session.delete(service)
        session.commit()
        return redirect(url_for('showService'))
    else:
        return render_template('deleteService.html', service = service)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)