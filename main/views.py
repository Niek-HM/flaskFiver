from flask import render_template, redirect, url_for, request, session, make_response

from handles.databaseHandle import ReadWrite
from handles.userHandle import User
from handles.sendEmailHandle import sendPersonal, sendMass
from handles.incryptionHandle import encrypt, checkHash

from werkzeug.utils import secure_filename

import random, os

# NOTE Initialize the database
database = ReadWrite()
userhandle = User(database)

dir_ = os.path.dirname(os.path.realpath(__file__)) # NOTE The path from the driver to this files current folder

# NOTE All the defenitions are linked through the app.py (the urls point here)
def homeView():
    user = userhandle.isLoggedIn(session) # NOTE Check if the user is logged in
    if user == []: return redirect(url_for('logout')) # NOTE Return to login page and remove session data if login check failed

    return render_template('home.html') # NOTE Return the correct html when everything checks out

def verifyView():
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))

    errors = [] # NOTE If any errors occur we will append it to this list

    if request.method == 'GET': # NOTE on a 'GET' request (The first time you load the page) this is called
        try: # NOTE Catch any exeptions so we know everything worked
            email = user[3]
            code = str(random.randint(100000, 999999)) # NOTE Generate a random code with a length of 6
            session['verify:code'] = encrypt(code) # NOTE encrypt the code and store it in the session
            sendPersonal(email, 'Varification Code', code) # NOTE send email with the code
            errors.append('A new code has been sent to you through email') # NOTE Show it was successfull through the error messages

        except Exception as e: # NOTE Catch any errors and append a message for the user
            print(e)
            errors.append('Something went wrong while creating the verification code, please reload the page to try again.') #! Return something for the popup json to receive

    if request.method == 'POST': # NOTE This runs when a form has been submitted
        code = request.values.get('code') # NOTE Get the 'code' input field from the form

        if checkHash(code, session['verify:code']): database.changeData('user', ['isSeller'], ['1']) # NOTE Check if the given code is correct and change the seller data in the database
        else: errors.append('The code did not match the one we provided through email.')

    return render_template('verify.html', errors=errors)


def adminView():
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))
    if user[2] == 0: return redirect(url_for('home')) # NOTE Return the user to the home page if he is not an admin

    all_table_names = database.read('sqlite_master', 'name', f"WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    
    for i in range(all_table_names.__len__()): #
        length = database.read(f"{all_table_names[i][0]}", '*')
        all_table_names[i] += (length.__len__(),)

    return render_template('admin.html', tables=all_table_names) # NOTE The tables=all_table_names makes sure we can get this data in the html

def adminSpecificView(specific):
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))
    if user[2] == 0: return redirect(url_for('home'))

    data = database.read(f'{specific}', '*') # NOTE get all the data from the selected database
    
    return render_template('adminView.html', data=data, table=specific)

#########################################################


def loginView():
    if 'id' in session and 'token' in session: return redirect(url_for('home')) # NOTE Go to the home page if the user is logged in

    if request.method == 'POST':
        errors, id, tokenSession = userhandle.userLogin(request) # NOTE log the user in if everything is valid

        if errors != []: return render_template('login.html', errors=errors) # NOTE In this case i don't want to proceed if any errors are found

        session['id'] = id # NOTE saves the id in the session data
        session['token'] = tokenSession # NOTE Saves the token in the session data

        return redirect(url_for('home'))

    return render_template('login.html', errors=[])

def logoutView():
    session.pop('token', None) # NOTE Clear token from the session data
    session.pop('id', None) # NOTE Clear the user dict from the session


    return redirect(url_for('login')) # Redirect to the login page

def registerView():
    if 'id' in session and 'token' in session: return redirect(url_for('home'))

    if request.method == 'POST':
        errors = userhandle.createUser(request) # NOTE Create a new user
        if errors != []: return render_template('register.html', errors=errors)

        return redirect(url_for('login'))
    
    return render_template('register.html', errors=[])

#! Not finished
def accountView(userToView):
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST': 
        # TODO Make changes to your account
        f = request.values.get('file')
        if f != '':
            path_ = f'{dir_}/static/img/user/pfp/{user[0]}/'
            if not os.path.exists(path_): os.makedirs(path_)

            path = f'{path_}.{user[0]}{secure_filename(f.filename).split(".")[-1]}' # FIXME Test if this overwrites the old pfp or just bugs out

            f.save((path)) # NOTE file name = userID_productname
        else: path = 'DEFAULT'
        
    
    if not userToView.isnumeric(): # NOTE Check if the input we gave is a name
        try: 
            userToView = list(database.read('user', 'id, name, pfp, first_name, last_name, email, phone, rating, website, github, insta, facebook, twitter, isSeller, privacy, isMod, isAdmin', f'WHERE name="{userToView}"')[0])
            if userToView[7] == 1: # NOTE Check if the user has set their account to private
                del userToView[3:6] # NOTE Deletes the last name, email and phone from the vieuwable list
                #del userToView[8] # FIXME Check if correct data is removed
        except IndexError: userToView = []

    else: # NOTE Otherwise the id is given
        try: 
            userToView = list(database.read('user', 'id, name, pfp, first_name, last_name, email, phone, rating, website, github, insta, facebook, twitter, isSeller, privacy, isMod, isAdmin', f'WHERE id="{userToView}"')[0])
            if userToView[7] == 1: del userToView[3:6]
        except IndexError: userToView = []

    products = []
    same = '0'
    if userToView != []: # NOTE If the user exists we will get all the products they have and find their profile picture
        userToView[2] = userToView[2] if userToView[2] != None else 'default.png'
        products = database.read('products', 'creator, img, description, title, body, price', f'WHERE creator="{userToView[0]}"') # Still need to get a rating
        same = '1' if userToView[0] == user[0] else '0'

    if userToView != []: return render_template('account.html', user=userToView, same=same, products=products)
    else: return render_template('notFound.html') # NOTE If no users where found we will return a custom page

def productView(id): 
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))

    product, images, comments, ratings, resp = [], [], [], [], False
    
    if id.isnumeric(): 
        try: 
            product = database.read('products', 'id, description, title, body, price, creator', f'WHERE id="{id}"')[0]

            # .sort(key=lambda i: i[1]) # NOTE Get all the images from the database and sort them by the pos value
            images = database.read('productimg', 'img, pos', f'WHERE product="{id}"')
            comments = database.read('comments', 'comenter, stars, comment, creation', f'WHERE for="{product[0]}"').sort(key=lambda i: i[3], reverse=True)
            ratings = database.read('ratings', 'rating', f'where for="{product[5]}"')
        except IndexError as e: 
            print(e)
            return render_template('notFound.html')

    
    rating = 0
    for i in ratings: rating += int(i[0])
    if ratings.__len__() > 0: rating = rating/ratings.__len__() # NOTE Make an avarage from all the received ratings
    else: rating = 'No ratings yet..' # FIXME Make this visible in the html

    # FIXME temp fix since not more then 1 image can be added right now
    images = (images[0], images[0], images[0], images[0], images[0])

    if request.method == 'POST':
        try: 
            if request.form['buy']:
                resp = make_response(redirect(url_for('buyproduct'))) # FIXME Check if this works!!!
                
                if 'buy' in request.cookies.keys(): resp.set_cookie(f'buy', f"{request.cookies.get('buy')},{id}")
                else: resp.set_cookie('buy', id)
                return resp

        except KeyError:
            if request.form['add']:
                resp = make_response(render_template('product_view.html', product=product, images=images, comments=comments, rating=rating))
                
                if 'buy' in request.cookies.keys(): resp.set_cookie(f'buy', f"{request.cookies.get('buy')},{id}")
                else: resp.set_cookie('buy', id)
                return resp # BUG This can still return an error if a users sends a post from some other program but this should not happen on this scale.

    return render_template('product_view.html', product=product, images=images, comments=comments, rating=rating)

def buyView(): # BUG Returns the products, prices etc, but you can't actually pay and it does not show on the screen
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))

    productlist = request.cookies.get('buy').split(',')

    strs = ''
    for i in productlist: # FIXME This is a temporary fix
        if i == '': continue
        elif strs == '': strs = f'id="{i}"'
        else: strs += f' OR id="{i}"'

    products = database.read('products', 'id, title, price', f'WHERE {strs}')
    
    total = 0
    for i in products:
        total += i[2] * productlist.count(str(i[0]))

    return render_template('buy_product.html', product=products, amount=total)

def searchView(search): 
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))

    if search == '*': search = ''
    search = search.split('_')
    cmd = ''
    
    for i in search: cmd += f'title LIKE "%{i}%" OR '
    cmd = cmd[:-4] # NOTE Removes the last or

    products = database.read('products', 'id, title, body, price', f'WHERE {cmd}')
    return render_template('searching.html', products=products, search=search)

def userlookupView(user):
    user_ = userhandle.isLoggedIn(session)
    if user_ == []: return redirect(url_for('logout'))

    if user == '*': user = ''
    users = database.read('user', 'pfp, name, first_name, last_name, isSeller', f'WHERE name LIKE "%{user}%"')
    return render_template('user_lookup.html', users=users, search=user)

def reportView(id):
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST':
        reported = request.values.get('user_').split(' - ')[0] # NOTE Get the id
        types = request.values.get('types') # NOTE Get the type of offence
        info = request.values.get('descr') # NOTE Get the description of the offence

        sendMass(receivers=['niekmeijlink@gmail.com', user[3]], head=f'Report from {user[3]}', body=f'<h1><b>Report submitted</b></h1><p> - {types}</p>\n\n<p>{info}</p>', file='')

        saved = database.write('reports', 'reported, reporter, types, info', [reported, user[0], types, info])
        if saved: return redirect(url_for('home'))
    
    if id.isnumeric(): # FIXME This only works for id's atm, later also allow for usernames
        user_ = database.read('user', 'id, name', f'WHERE id="{id}"')[0]
        users = database.read('user', 'id, name', f'WHERE NOT id="{id}"')
        return render_template('report.html', user=user_, users=users)
    
    else: return redirect(url_for('home'))

def createProductView():
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST':
        errors = []
        title = request.values.get('title')
        
        f = request.files['file'] # NOTE Get file from form and save it
        if f != '':
            path_ = f'{dir_}/static/img/products/{user[0]}/'
            if not os.path.exists(path_): os.makedirs(path_)

            path = f'{path_}{user[0]}_{title}.{secure_filename(f.filename).split(".")[-1]}'

            if os.path.exists(path): errors.append('You already have a product with this title.')
            else: f.save((path)) # NOTE file name = userID_productname
        else: path = 'DEFAULT'

        short_descr = request.values.get('short-descr')
        body = request.values.get('body')
        price = request.values.get('price')

        if not short_descr or not body or not price: errors.append('Make sure all fields where correctly filled in.')

        if errors: return render_template('create_product.html', errors=errors)

        path = path.split('/')[-1] # NOTE Only save the filename
        saved1 = database.write('products', 'description, title, body, price, creator', [short_descr, title, body, price, user[0]])
        saved2 = database.write('productimg', 'product, img, pos', [database.cursor.lastrowid, path, 0])
        
        if saved1 and saved2: return redirect(url_for('home')) # BUG Should go to the product instead of home
        else: return render_template('create_product.html', errors=['There was an error when saving to the database.']) # FIXME Should check on wich save the error was

    return render_template('create_product.html', errors=[])

#! It works, just don't forget to make the body a bit larger
def contactView():
    user = userhandle.isLoggedIn(session)
    if user == []: return redirect(url_for('logout'))

    errors = []

    if request.method == 'POST':
        title = request.values.get('title')
        body = request.values.get('body')
        if title == '' or body == '': errors.append('Make sure all fields are filled in before trying to send anything.') 
        else: 
            sendMass([user[3], 'niekmeijlink@gmail.com'], title, body)
            errors.append('Email was sent successfully, please check your email for confirmation')

    return render_template('contact_us.html', errors=errors)