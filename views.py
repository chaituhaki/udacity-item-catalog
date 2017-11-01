from flask import Flask, url_for, render_template, jsonify, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database_setup import Base, Genre, Item

engine = create_engine("sqlite:///AnimeCatalog.db")

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
app = Flask(__name__)

@app.route('/')
@app.route('/genre/')
def showGenre():
    genre = session.query(Genre).all()
    item = session.query(Item).filter_by(id = 1).all()
    return render_template('home.html', genre = genre, item = item)

@app.route('/genre/<int:genre_id>/items/')
def showItems(genre_id):
    allGenre = session.query(Genre).all()
    genre = session.query(Genre).filter_by(id = genre_id).one()
    item = session.query(Item).filter_by(genre_id = genre_id).all()
    return render_template('items.html', genre = genre, item = item, allGenre = allGenre)

#Add new Item
@app.route('/genre/<int:genre_id>/items/new/', methods =['GET', 'POST'])
def newItem(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    #POST request
    if request.method == 'POST':
        if request.form['name']:
            item = Item(name = request.form['name'], genre_id = genre_id)
            session.add(item)
            session.commit()
            return redirect(url_for('showItems', genre_id = genre_id))
        else:
            alert = 'alert("Fill all required field")'
            return render_template('newItem.html', alert= alert, genre = genre)
    #GET request
    else:
        return render_template('newItem.html', genre = genre)

#EDIT a Item
@app.route('/genre/<int:genre_id>/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(genre_id, item_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    #POST request
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
            session.add(item)
            session.commit()
        return redirect(url_for('showItems', genre_id = genre_id))
    #GET request
    else:
        return render_template('editItem.html', item = item)

@app.route('/genre/<int:genre_id>/items/<int:item_id>/delete/', methods =['GET', 'POST'])
def deleteItem(genre_id, item_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    #POST request
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItems', genre_id = genre_id))
    #GET request
    else:
        return render_template('deleteItem.html', item = item, genre = genre)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)