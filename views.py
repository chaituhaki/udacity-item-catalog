from flask import Flask, url_for, render_template, jsonify, request, redirect
from flask import session as login_session, flash
from flask_httpauth import HTTPBasicAuth

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database_setup import Base, Genre, Item, User

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import random, string

engine = create_engine("sqlite:///AnimeCatalog.db")

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        print("token")
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Hi, already logged in'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    
    return jsonify(name=login_session['username'], email=login_session['email'],
                   img=login_session['picture'])

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session[
                   'picture'], provider=login_session['provider'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def create_state():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return state


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
	
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


@app.route('/')
@app.route('/genre/')
def showGenre():
    state = create_state()
    allGenre = session.query(Genre).all()
    item = session.query(Item).filter_by(id=1).all()
    state = create_state()
    return render_template('home.html', allGenre=allGenre, item=item, STATE=state)


@app.errorhandler(404)
def page_not_found(error):
    return '404. This page does not exist', 404


@app.route('/genre.json/')
def get_genre():
    """
    returns json that contains all genre categories
    """
    if 'username' not in login_session['username']:
        return redirect('/login')
    genre = session.query(Genre).all()
    return jsonify(genre=[g.serialize for g in genre])


@app.route('/items.json/')
def get_items():
    """
    returns json that contains all anime items
    """
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/genre/<int:genre_id>/items/')
def showItems(genre_id):
    allGenre = session.query(Genre).all()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    item = session.query(Item).filter_by(genre_id=genre_id).all()
    return render_template('items.html', genre=genre,
                           item=item, allGenre=allGenre)


# Add new Item
@app.route('/genre/<int:genre_id>/items/new/', methods=['GET', 'POST'])
def newItem(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    # POST request
    if request.method == 'POST':
        if request.form['name']:
            item = Item(name=request.form['name'], genre_id=genre_id)
            session.add(item)
            session.commit()
            return redirect(url_for('showItems', genre_id=genre_id))
        else:
            alert = 'alert("Fill all required field")'
            return render_template('newItem.html', alert=alert, genre=genre)
    # GET request
    else:
        return render_template('newItem.html', genre=genre)


# EDIT a Item
@app.route('/genre/<int:genre_id>/items/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(genre_id, item_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    # POST request
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
            session.add(item)
            session.commit()
        return redirect(url_for('showItems', genre_id=genre_id))
    # GET request
    else:
        return render_template('editItem.html', item=item)


@app.route('/genre/<int:genre_id>/items/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(genre_id, item_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    # POST request
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItems', genre_id=genre_id))
    # GET request
    else:
        return render_template('deleteItem.html', item=item, genre=genre)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
