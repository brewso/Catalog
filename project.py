#!/usr/bin/env python3
from flask import (Flask, render_template, redirect, request, jsonify,
                   url_for, flash, make_response)
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Category, User, CategoryItem
import random
import string
import json
import requests
import httplib2
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "catalog app"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login routes and functions
@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?grant_type='
           'fb_exchange_token&client_id=%s&client_secret=%s&'
           'fb_exchange_token=%s' % (app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we
        have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace the
        remaining quotes with nothing so that it can be used directly in the
        graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = ('https://graph.facebook.com/v2.8/me?'
           'access_token=%s&fields=name,id,email' % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = ('https://graph.facebook.com/v2.8/me/picture?access_token=%s&'
           'redirect=0&height=200&width=200' % access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    response = make_response(json.dumps('Login was successful!'),
                             200)
    response.headers['Content-Type'] = 'application/json'
    flash("Now logged in as %s" % login_session['username'])
    return response


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token=%s' %
           facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return


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
    url = ('https://www.googleapis.com/oauth2/v1/'
           'tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                    'Current user is already connected.'), 200)
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

    login_session['provider'] = 'google'
    if data['name']:
        login_session['username'] = data['name']
    else:
        login_session['username'] = data['email']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    response = make_response(json.dumps('Login was successful!'),
                             200)
    response.headers['Content-Type'] = 'application/json'
    flash("Now logged in as %s" % login_session['username'])
    return response


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None


def userIsLoggedIn():
    if 'username' not in login_session:
        return False
    else:
        return True


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/'
           'revoke?token=%s' % access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


# JSON APIs to view Restaurant Information
@app.route('/category/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


@app.route('/category/<int:category_id>/<int:categoryitem_id>/JSON')
def categoryItemJSON(category_id, categoryitem_id):
    item = session.query(CategoryItem).filter_by(id=categoryitem_id).one()
    return jsonify(CategoryItem=item.serialize)


@app.route('/catalog/JSON')
def catalogJSON():
    catalog = session.query(Category).all()
    return jsonify(catalog=[c.serialize for c in catalog])


# start of app landing pages
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category)
    return render_template('catalog.html',
                           categories=categories)


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():
    if userIsLoggedIn() is False:
        return redirect(url_for('login'))
    if request.method == 'POST' and request.form['name'] != '':
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newcategory.html')


@app.route('/category/<int:category_id>')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return render_template('category.html',
                           category=category,
                           items=items)


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if userIsLoggedIn() is False:
        return redirect(url_for('login'))
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    # if the user id doesnt match to the creator of category redirect
    if login_session['user_id'] != editedCategory.user_id:
        print("You are not the authorized user!")
        return redirect(url_for('showCategory',
                                category_id=category_id))
    if request.method == 'POST' and request.form['name'] != '':
        flash(request.form['name'])
        editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        return redirect(url_for('showCategory',
                                category_id=editedCategory.id))
    else:
        return render_template('editcategory.html',
                               category=editedCategory)


@app.route('/category/<int:category_id>/delete', methods=['POST', 'GET'])
def deleteCategory(category_id):
    if userIsLoggedIn() is False:
        return redirect(url_for('login'))
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(category_id=category_id)
    # if the user id doesnt match to the creator of category redirect
    if login_session['user_id'] != category.user_id:
        flash("You are not the authorized user!")
        return redirect(url_for('showCategory',
                        category_id=category_id))
    if request.method == 'POST':
        session.delete(category)
        for item in items:
            session.delete(item)
        session.commit()
        return redirect(url_for('showCatalog'))
    return render_template('deletecategory.html',
                           category=category)


@app.route('/category/<int:category_id>/new', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if userIsLoggedIn() is False:
        return redirect(url_for('login'))
    category = session.query(Category).filter_by(id=category_id).one()
    # if the user id doesnt match to the creator of category redirect
    if login_session['user_id'] != category.user_id:
        flash("You are not the authorized user!")
        return redirect(url_for('showCategory',
                        category_id=category_id))
    if (request.method == 'POST'
            and request.form['name'] != ''
            and request.form['description'] != ''):
        newItem = CategoryItem(name=request.form['name'],
                               description=request.form['description'],
                               user_id=login_session['user_id'],
                               category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    return render_template('newcategoryitem.html', category=category)


@app.route('/category/<int:category_id>/<int:categoryitem_id>/edit',
           methods=['POST', 'GET'])
def editCategoryItem(category_id, categoryitem_id):
    if userIsLoggedIn() is False:
        return redirect(url_for('login'))
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(CategoryItem).filter_by(id=categoryitem_id).one()
    # if the user id doesnt match to the creator of item redirect
    if login_session['user_id'] != item.user_id:
        flash("You are not the authorized user!")
        return redirect(url_for('showCategory',
                        category_id=category_id))
    if (request.method == 'POST'
            and request.form['name'] != ''
            and request.form['description'] != ''):
        item.name = request.form['name']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        return redirect(url_for('showCategory',
                        category_id=category_id))
    else:
        return render_template('editCategoryItem.html',
                               item=item,
                               category=category)


@app.route('/category/<int:category_id>/<int:categoryitem_id>/delete',
           methods=['POST', 'HEAD', 'GET'])
def deleteCategoryItem(category_id, categoryitem_id):
    if userIsLoggedIn() is False:
        return redirect(url_for('login'))
    item = session.query(CategoryItem).filter_by(id=categoryitem_id).one()
    # if the user id doesnt match to the creator redirect
    if login_session['user_id'] != item.user_id:
        flash("You are not the authorized user!")
        return redirect(url_for('showCategory',
                                category_id=item.category_id))
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showCategory',
                                category_id=item.category_id))
    return render_template('deletecategoryitem.html',
                           item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
