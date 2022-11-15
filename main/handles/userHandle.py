from handles.incryptionHandle import encrypt, checkHash

from uuid import uuid4  # For generating a new token

allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@[]^_{|}~'

class User:
    def __init__(self, database): self.database = database

    def isLoggedIn(self, token, id):
        user = self.database.read(tables='user', rows='id, token, isAdmin', specification=f'WHERE id="{id}"')[0] # Get the user with the same id

        if not checkHash(user[1], token): return [] # Check if the token is valid #!Not sure if the [0] is needed

        return user
    
    def userLogin(self, request=None): # Get the login form data and check if its valid
        if request == None: return ['No request data found.?'], None, None
        errors = []

        username = request.values.get('username')
        password = request.values.get('password')

        if username == '': errors.append('Username field can not be empty.')
        if password == '': errors.append('Password field can not be empty.')
                
        for i in (password+username):
            if i not in allowed_chars:
                errors.append(f'Invalid character(s) found.')
                break

        if errors != []: return errors, None, None

        user = self.database.read(tables='user', rows='id, name, passwordHash, token', specification=f'WHERE name="{username}"') # Always returns a list in the format: [id, name, passwordHash, token]
        
        if user != [] and checkHash(password, user[0][2]): return [], user[0][0], encrypt(user[0][3]) # The token get encrypted so no one can steal it later # errors, user, id, token *We incrypt the token to prevent ppl from stealing it out of your browser..

        return ['Username or password is wrong.'], None, None
    
    def createUser(self, request=None):
        if request == None: return ['No request data found.?'], None, None
        errors = []

        username = request.values.get('username')
        password = request.values.get('password')

        for i in (password+username):
            if i not in allowed_chars: #* Only checks if every character is in a specific list of chars
                errors.append(f'Invalid character(s) found.')
                break

        if username == '': errors.append('Username field can not be empty.')
        if password == '': errors.append('Password field can not be empty.')
        elif password.__len__() < 5: errors.append('Password needs at least 5 characters.')
                
        if errors != []: return errors
        
        user = self.database.read(tables='user', rows='name', specification=f'WHERE name="{username}"')
        
        if user.__len__() != 0: return ['Username is already taken.'] #! Checks if no users are returned (This can only happen if the username is taken)

        success = self.database.write('user', 'name, passwordHash, token', [username, encrypt(password), str(uuid4())])

        if success: return [] # This should be True if the user was successfully saved
        return ['An error occured when saving to the database.']