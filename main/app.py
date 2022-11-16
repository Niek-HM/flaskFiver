from flask import Flask, session # Flask is our host
from views import *

import bcrypt 

from handles.databaseHandle import Create, ReadWrite
Create() # Make sure all databases exist

from waitress import serve

class MainApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = bcrypt.gensalt() # Generates a different salt every time the server is run

        self.get_possible_urls()

        serve(self.app, host='0.0.0.0', port=5000, threads=4) # Default threads=4 but it 
    
    def get_possible_urls(self):
        self.app.add_url_rule('/', 'home', homeView, methods=['GET', 'POST'])
        self.app.add_url_rule('/admin/', 'admin', adminView, methods=['GET', 'POST'])
        self.app.add_url_rule('/admin/<specific>/', 'adminView', adminSpecificView, methods=['GET', 'POST'])
        
        # For searching: self.app.add_url_rule('/search?q=<search>/', 'search', searchView, methods=['GET', 'POST'])
        # For searching: self.app.add_url_rule('/users?q=<search>/', 'searchusers', searchUsersView, methods=['GET', 'POST'])
            
        self.app.add_url_rule('/login/', 'login', loginView, methods=['GET', 'POST'])
        self.app.add_url_rule('/logout/', 'logout', logoutView, methods=['GET', 'POST'])
        self.app.add_url_rule('/register/', 'register', registerView, methods=['GET', 'POST'])

        self.app.add_url_rule('/account/<userToView>/', 'account', accountView, methods=['GET', 'POST'])
        self.app.add_url_rule('/product/<id>/', 'viewproduct', productView, methods=['GET', 'POST'])
        self.app.add_url_rule('/buy/<productID>/', 'buyproduct', buyView, methods=['GET', 'POST'])
        self.app.add_url_rule('/search?q=<search>/', 'search', searchView, methods=['GET', 'POST'])
        self.app.add_url_rule('/user?q=<user>/', 'userlookup', userlookupView, methods=['GET', 'POST'])
        self.app.add_url_rule('/report/<id>/', 'report', reportView, methods=['GET', 'POST'])
        
        """ 
        * This are some pages i want to add, look in TODO to find named html files (with no content though)
        
        * Change password should be added
        * More pages for the users account
        * More pages to view reports you gave
        * Some admin pages to manage reports, ban people, etc
        ! Think of more items that are needed later
        """

if __name__ == '__main__':
    MainApp()#.app.run('0.0.0.0', 5000, debug=False) # options=....
    #* Atm waitress.serve() runs the server on the local wifi, anyone can access by typing in your ip...