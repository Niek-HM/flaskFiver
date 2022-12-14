from flask import render_template, redirect, url_for, request, session

from handles.databaseHandle import ReadWrite
from handles.userHandle import User
from handles.sendEmailHandle import sendPersonal, sendMass
from handles.incryptionHandle import encrypt, checkHash

from werkzeug.utils import secure_filename

import random, os

#* Open the database and initialize the user class
database = ReadWrite()
userhandle = User(database)

dir_ = os.path.dirname(os.path.realpath(__file__))

# All the def's are connected to the url rules in app.py
def homeView():
    user = userhandle.isLoggedIn(session) # Check if the user is logged in
    if user == []: return redirect(url_for('logout')) # Redirect to the logout page so the user can correctly log in

    if request.method == 'POST': #! Atm all post requests will be for vendor stuff
        try: 
            email = user[3]
            code = str(random.randint(100000, 999999)) # Generate a random code
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

    return render_template('login.html', errors=[])

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
    
    return render_template('register.html', errors=[])


#! All below don't have any html in them
'''
    if 'token' not in session or 'id' not in session: return redirect(url_for('logout')) # Go to the login screen if there is no token or user found
    user = userhandle.isLoggedIn(session['token'], session['id']) # Check if the session data is valid
    if user == []: return redirect(url_for('logout')) # No user object was returned so we clear the session data and go to login

'''

def accountView(userToView):
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST': 
        pass #! Make changes to their account
        # username = ...
        # pfp = ...
        # etc....
    
    if not userToView.isnumeric(): 
        try: 
            userToView = list(database.read('user', 'id, name, pfp, first_name, last_name, email, phone, rating, website, github, insta, facebook, twitter, isSeller, privacy, isMod, isAdmin', f'WHERE name="{userToView}"')[0])
            if userToView[7] == 1: 
                del userToView[3:5] # Deletes the 4- and 5th item form the list
                del userToView[8]
        except IndexError: userToView = []

    else: 
        try: userToView = list(database.read('user', 'id, name, pfp, first_name, last_name, email, phone, rating, website, github, insta, facebook, twitter, isSeller, privacy, isMod, isAdmin', f'WHERE id="{userToView}"')[0])
        except IndexError: userToView = []

    products = []
    same = '0'
    if userToView != []:
        userToView[2] = userToView[2] if userToView[2] != None else 'default.png'
        products = database.read('products', 'creator, img, description, title, body, price', f'WHERE creator="{userToView[0]}"') # Still need to get a rating
        same = '1' if userToView[0] == user[0] else '0'

    if userToView != []: return render_template('account.html', user=userToView, same=same, products=products)
    else: return render_template('notFound.html')

##! Most stuff below still needs to check for POST or GET and do some more specific stuff, i just did the basic database reads that where needed

def productView(id): 
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    try:
        product, images = [], []
        if id.isnumeric(): product = database.read('products', 'id, description, title, body, price', f'WHERE id="{id}"')[0] #! Allow multiple images
        else: pass #* Search by name or somthing??

        if product !=[]: images = database.read('productimg', 'product, img, pos', f'WHERE product IN {product}')
        return render_template('product_view.html', product=product, images=images)
    except: return render_template('notFound.html')

def buyView(id): #! One of the last things to do, don't forget haha
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    return render_template('but_product.html', product=id)

def searchView(search): 
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    if search == '*': search = ''
    search = search.split('_')
    cmd = ''
    for i in search: cmd += f'title LIKE "%{i}%" OR '
    cmd = cmd[:-4] #* Remove the last or and spaces

    products = database.read('products', 'id, title, body, price', f'WHERE {cmd}') #! Not tested if this works
    return render_template('searching.html', products=products, search=search)

def userlookupView(user): #* This is the most basic version i can make
    user_ = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user_ == []: return redirect(url_for('logout'))

    if user == '*': user = ''
    users = database.read('user', 'pfp, name, first_name, last_name, isSeller', f'WHERE name LIKE "%{user}%"')
    return render_template('user_lookup.html', users=users, search=user)

def reportView(id):
    user = userhandle.isLoggedIn(session)  # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST':
        reported = request.values.get('user_').split(' - ')[0] #* Get the id
        types = request.values.get('types')
        info = request.values.get('descr')
        #! Improve the styling later
        sendMass(receivers=['niekmeijlink@gmail.com', user[3]], head=f'Report from {user[3]}', body=f'<h1><b>Report submitted</b></h1><p> - {types}</p>\n\n<p>{info}</p>', file='')

        saved = database.write('reports', 'reported, reporter, types, info', [reported, user[0], types, info])
        if saved: return redirect(url_for('home'))
    
    if id.isnumeric():
        user_ = database.read('user', 'id, name', f'WHERE id="{id}"')[0]
        users = database.read('user', 'id, name', f'WHERE NOT id="{id}"')
        return render_template('report.html', user=user_, users=users)
    
    else: return redirect(url_for('home')) #* Do something else

def createProductView():
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST':
        errors = []
        title = request.values.get('title')
        
        f = request.files['file']
        if f != '':
            path = f'{dir_}/static/products/{user[0]}_{title}.{secure_filename(f.filename).split(".")[-1]}'

            if os.path.exists(path): errors.append('You already have a product with this name')
            else: f.save((path)) #*id+product_name+type
        else: path = 'DEFAULT'

        short_descr = request.values.get('short-descr')
        body = request.values.get('body')
        price = request.values.get('price')

        if not short_descr or not body or not price: errors.append('Make sure all fields where correctly filled in.')

        if errors: return render_template('create_product.html', errors=errors)

        path = path.split('/')[-1] # Only save the filename
        saved = database.write('products', 'img, description, title, body, price, creator', [path, short_descr, title, body, price, user[0]])
        
        if saved: return redirect(url_for('home')) #! Should reroute to the product itself
        else: return render_template('create_product.html', errors=['There was an error when saving to the database.'])

    return render_template('create_product.html', errors=[])

def contactView():
    user = userhandle.isLoggedIn(session) # Check if the session data is valid
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST':
        pass # Send email

    return render_template('contact_us.html')