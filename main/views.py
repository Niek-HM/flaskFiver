from flask import render_template, redirect, url_for, request, session

from handles.databaseHandle import ReadWrite
from handles.userHandle import User
from handles.sendEmailHandle import sendPersonal
from handles.incryptionHandle import encrypt, checkHash

from werkzeug.utils import secure_filename

import random, os

database = ReadWrite()
userhandle = User(database)

def homeView():
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout')) # No user object was returned so we clear the session data and go to login

    if request.method == 'POST': #! Atm all post requests will be for vendor stuff
        try: 
            email = user[3] # Send an email with username etc
            code = str(random.randint(100000, 999999))
            sendPersonal(email, 'Varification Code', code)
            session['code'] = encrypt(code)
            return redirect(url_for('verify'))

        except Exception: worked = False #! Return something for the popup json to receive
    else: worked = None
    return render_template('home.html', worked=worked) # The user is logged in so we show the page

def verifyView():
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout')) # No user object was returned so we clear the session data and go to login

    if request.method == 'POST':
        code = request.values.get('code')
        if checkHash(code, session['code']): 
            print('Corect code was given') #! Set vendor value to true

    return render_template('verify.html')


def adminView():
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))
    if user[2] == 0: return redirect(url_for('home'))

    all_table_names = database.customRead("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    
    for i in range(all_table_names.__len__()):
        length = database.read(f"{all_table_names[i][0]}", '*')
        all_table_names[i] += (length.__len__(),)

    return render_template('admin.html', tables=all_table_names)

def adminSpecificView(specific):
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    
    if user == []: return redirect(url_for('logout'))
    if user[2] == 0: return redirect(url_for('home'))

    data = database.read(f'{specific}', '*')
    
    return render_template('adminView.html', data=data, table=specific)

#########################################################


def loginView():
    if 'id' in session and 'token' in session: return redirect(url_for('home')) # Go to the home page if the user is logged in

    if request.method == 'POST': # The user has submitted the form
        errors, id, tokenSession = userhandle.userLogin(request)

        if errors != []: return render_template('login.html', errors=errors) # An error was found in the form

        session['id'] = id # saves the id in the session data
        session['token'] = tokenSession # Saves the token in the session data

        return redirect(url_for('home'))

    else: return render_template('login.html', errors=[])

def logoutView():
    session.pop('token', None) # Clear token from the session data
    session.pop('id', None) # Clear the user dict from the session


    return redirect(url_for('login')) # Redirect to the login page

def registerView():
    if 'id' in session and 'token' in session: return redirect(url_for('home')) # Go to the home page if the user is logged in

    if request.method == 'POST':
        errors = userhandle.createUser(request)
        if errors != []: return render_template('register.html', errors=errors)

        return redirect(url_for('login'))
    
    else: return render_template('register.html', errors=[])


#! All below don't have any html in them
'''
    if 'token' not in session or 'id' not in session: return redirect(url_for('logout')) # Go to the login screen if there is no token or user found
    user = userhandle.isLoggedIn(session['token'], session['id']) # Check if the session data is valid
    if user == []: return redirect(url_for('logout')) # No user object was returned so we clear the session data and go to login

'''

def accountView(userToView):
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST': pass #! Make changes to their account
    
    if not userToView.isnumeric(): 
        try: userToView = database.read('user', '*', f'WHERE name="{userToView}"')[0]
        except IndexError: userToView = []

    else: 
        try: userToView = database.read('user', '*', f'WHERE id="{userToView}"')[0]
        except IndexError: userToView = []
    
    same = False
    if userToView == user: same = True

    if userToView != []: return render_template('account.html', user=userToView, same=same)
    else: return render_template('accountNotFound.html')

##! Most stuff below still needs to check for POST or GET and do some more specific stuff, i just did the basic database reads that where needed

def productView(productID): 
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    product = database.read('products', 'id, title, body, price', f'WHERE id LIKE "%{productID}%"')
    return render_template('product_view.html', product=product)

def buyView(productId): #! One of the last things to do, don't forget haha
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    return render_template('but_product.html', product=productId)

def searchView(search): 
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    search = search.split(' ')
    cmd = ''
    for i in search: cmd += f'title LIKE "%{i}%" OR '
    cmd = cmd[:-4] #* Remove the last or and spaces

    products = database.read('products', 'id, title, body, price', f'WHERE {cmd}') #! Not tested if this works
    return render_template('searching.html', search=products)

def userlookupView(user): #* This is the most basic version i can make
    user_ = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user_ == []: return redirect(url_for('logout'))

    if user == '*': user = ''
    users = database.read('user', 'pfp, name, first_name, last_name, isSeller', f'WHERE name LIKE "%{user}%"')
    return render_template('user_lookup.html', users=users, search=user)

def reportView(id): #! This needs an overhoul, pls do later when you are more sure
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    report = database.read('reports', 'id, reported, reporter, types, info', f'WHERE id="{id}"')
    return render_template('report.html', id=report)

def createProductView():
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST':
        errors = []
        title = request.value.get('title')
        
        f = request.files['file']
        path = f'/static/products/{user[1]}/{title}.{secure_filename(f.filename).split(".")[-1]}'

        if os.path.exists(path): errors.append('You already have a product with this name')
        else: f.save((path)) #*id+product_name+type

        short_descr = request.values.get('short-descr')
        body = request.values.get('body')
        price = request.values.get('price')

        if errors: return render_template('create_product.html', errors=errors)

        saved = database.write('products', 'img, description, title, body, price', [path, short_descr, title, body, price])
        
        if saved: return redirect(url_for('home')) #! Should reroute to the product itself
        else: return render_template('create_product.html', errors=['There was an error when saving to the database.'])

    return render_template('create_product.html', errors=[])