from distutils.log import error
from flask import render_template, redirect, url_for, request, session

from handles.databaseHandle import ReadWrite
from handles.userHandle import User
from handles.incryptionHandle import encrypt, checkHash
from handles.sendEmailHandle import sendPersonal

import random

database = ReadWrite()
userhandle = User(database)

def homeView():
    if 'token' not in session or 'id' not in session: return redirect(url_for('logout')) # Go to the login screen if there is no token or user found
    user = userhandle.isLoggedIn(session['token'], session['id']) # Check if the session data is valid
    if user == []: return redirect(url_for('logout')) # No user object was returned so we clear the session data and go to login

    if request.method == 'POST': #! Atm all post requests will be for vendor stuff
        try: 
            email = user[3] # Send an email with username etc
            code = random.randint(100000, 999999)
            sendPersonal(email, 'Varification Code', code)
            return redirect(url_for('verify'), code=code)

        except Exception: worked = False #! Return something for the popup json to receive
    else: worked = None
    return render_template('home.html', worked=worked) # The user is logged in so we show the page

def adminView():
    if 'token' not in session or 'id' not in session: return redirect(url_for('logout'))
    user = userhandle.isLoggedIn(session['token'], session['id'])
    if user == []: return redirect(url_for('logout'))
    if user[2] == 0: return redirect(url_for('home'))

    all_table_names = database.customRead("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    
    for i in range(all_table_names.__len__()):
        length = database.read(f"{all_table_names[i][0]}", '*')
        all_table_names[i] += (length.__len__(),)

    return render_template('admin.html', tables=all_table_names)

def adminSpecificView(specific):
    if 'token' not in session or 'id' not in session: return redirect(url_for('logout'))
    user = userhandle.isLoggedIn(session['token'], session['id'])
    
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
    if 'token' not in session or 'id' not in session: return redirect(url_for('logout'))
    user = userhandle.isLoggedIn(session['token'], session['id'])
    if user == []: return redirect(url_for('logout'))

    if request.method == 'POST': pass #! Make changes to their account
    
    if not userToView.isnumeric(): 
        try: userToView = database.read('user', '*', f'WHERE name="{userToView}"')[0]
        except IndexError: userToView = []

    else: 
        try: userToView = database.read('user', '*', f'WHERE id="{userToView}"')[0]
        except IndexError: userToView = []
    
    same = 0
    if userToView == user: same = 1

    if userToView != []: return render_template('account.html', user=userToView, same=same)
    else: return render_template('accountNotFound.html')

def productView(productID): return render_template('product_view.html')
def buyView(productId): return render_template('but_product.html')
def searchView(search): return render_template('searching.html')

def userlookupView(user): #* This is the most basic version i can make
    if user == '*': user = ''
    users = database.read('user', 'pfp, name, first_name, last_name, isSeller', f'WHERE name LIKE "%{user}%"')
    return render_template('user_lookup.html', users=users, search=user)

def reportView(id): return render_template('report.html')