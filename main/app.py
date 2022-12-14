from flask import Flask, session # Flask is our host
from views import *

import bcrypt 

from handles.databaseHandle import Create, ReadWrite
Create() # Make sure all databases exist

from waitress import serve # I use this instead of flask is because waitress automatically hosts it locally

class MainApp:
    def __init__(self): #* Initialize the app and define all data
        self.app = Flask(__name__)
        self.app.secret_key = bcrypt.gensalt() # Generates a different salt every time the server is run so cookies won't always work properly

        self.get_possible_urls() #* Add the url rules

        serve(self.app, host='0.0.0.0', port=5000, threads=4) # Host the application
    
    def get_possible_urls(self): #* Add url rules (The all the sub places you can go to)
        self.app.add_url_rule('/', 'home', homeView, methods=['GET', 'POST'])
        self.app.add_url_rule('/admin/', 'admin', adminView, methods=['GET', 'POST'])
        self.app.add_url_rule('/admin/<specific>/', 'adminView', adminSpecificView, methods=['GET', 'POST'])
            
        self.app.add_url_rule('/login/', 'login', loginView, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout/', 'logout', logoutView, methods=['GET', 'POST'])
        self.app.add_url_rule('/register/', 'register', registerView, methods=['GET', 'POST'])

        self.app.add_url_rule('/account/<userToView>/', 'account', accountView, methods=['GET', 'POST'])
        self.app.add_url_rule('/product/<id>/', 'viewproduct', productView, methods=['GET', 'POST'])
        self.app.add_url_rule('/buy/<id>/', 'buyproduct', buyView, methods=['GET', 'POST'])
        self.app.add_url_rule('/search/<search>/', 'search', searchView, methods=['GET', 'POST'])
        self.app.add_url_rule('/user/<user>/', 'userlookup', userlookupView, methods=['GET', 'POST'])
        self.app.add_url_rule('/report/<id>/', 'report', reportView, methods=['GET', 'POST'])
        self.app.add_url_rule('/verify/', 'verify', verifyView, methods=['GET', 'POST'])
        self.app.add_url_rule('/create_product/', 'create-product', createProductView, methods=['GET', 'POST'])
        
        self.app.add_url_rule('/contact_us/', 'contact', contactView, methods=['GET', 'POST'])

if __name__ == '__main__':
    MainApp()#.app.run('0.0.0.0', 5000, debug=False) # options=....
    #* Atm waitress.serve() runs the server on the local wifi, anyone can access by typing in your ip...