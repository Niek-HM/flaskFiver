from handles.incryptionHandle import encrypt, checkHash

from uuid import uuid4  # NOTE Generates a uuid for every new user

# NOTE Set a list of characters we allow for username, password etc
allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@[]^_{|}~'

class User:
    def __init__(self, database): self.database = database

    def isLoggedIn(self, session): # NOTE Check if the user is logged in
        if 'token' not in session or 'id' not in session: return []
        
        ##* GET SESSION DATA AND CHECK IF IT IS VALID *##
        token, id = session['token'], session['id']
        try: 
            user = self.database.read(tables='user', rows='id, token, isAdmin, email', specification=f'WHERE id="{id}"')[0]
        except IndexError: return []
        
        if not checkHash(user[1], token): return []

        return user
    
    def userLogin(self, request=None): # NOTE allow for users to log in
        ##* CHECK IF ALL DATA IS PRESENT *##
        if request == None: return ['No request data found.?'], None, None
        errors = []

        username = request.values.get('username')
        password = request.values.get('password')

        if username == '': errors.append('Username field can not be empty.')
        if password == '': errors.append('Password field can not be empty.')

        if errors != []: return errors, None, None

        ##* CHECK IF THE USER EXISTS *##
        user = self.database.read(tables='user', rows='id, name, passwordHash, token', specification=f'WHERE name="{username}"')
        
        if user != [] and checkHash(password, user[0][2]): return [], user[0][0], encrypt(user[0][3])

        return ['Username or password is wrong.'], None, None
    
    def createUser(self, request=None): # NOTE Allow users to register
        ##* CHECK IF ALL DATA IS PRESENT *##
        if request == None: return ['No request data found.?'], None, None
        errors = []

        username = request.values.get('username')
        password = request.values.get('password')
        conf_password = request.values.get('confirm-password')
        first_name = request.values.get('first-name')
        last_name = request.values.get('last-name')
        email = request.values.get('email')

        if username == '': errors.append('Username field can not be empty.')
        if password == '': errors.append('Password field can not be empty.')
        elif password.__len__() < 5: errors.append('Password needs at least 5 characters.')
        if email == '': errors.append('Email field can not be empty.')

        ##* CHECK IF ALL THE DATA IS VALID *##
        if conf_password != password: errors.append('Password and Confirm Password are not the same')

        for i in (password+username+first_name+last_name+email+conf_password):
            if i not in allowed_chars:
                errors.append(f'Invalid character(s) found.')
                break
        
        letters = 0
        for i in username:
            if i not in '1234567890': letters += 1
        
        if letters == 0: errors.append('Your username must contain alphabetical characters.')
                
        if errors != []: return errors
        
        user = self.database.read(tables='user', rows='name', specification=f'WHERE name="{username}"')
        
        if user.__len__() != 0: return ['Username is already taken.']
        
        ##* SAVE THE ACCOUNT *##
        success = self.database.write('user', 'name, passwordHash, token, first_name, last_name, email, pfp', [username, encrypt(password), str(uuid4()), first_name, last_name, email, '']) # Maybe allow pfp to be chosen here?

        if success: return []
        return ['An error occured when saving to the database.'] # NOTE Returns an error if it was not saved correctly