from main.handles.databaseHandle import ReadWrite
from main.handles.incryptionHandle import encrypt, checkHash

from uuid import uuid4  # For generating a new token

database = ReadWrite()

def createUser():
    name = input('Username >> ')
    password = input('Password >> ')
    first_name = input('First Name >> ')
    last_name = input('Last Name >> ')

    is_seller = input('Is Seller >> ')
    is_admin = input('Is Admin >> ')
    is_mod = input('Is Mod >> ')

    database.write('user', 'name, passwordHash, token, first_name, last_name, isSeller, isAdmin, isMod', [name, encrypt(password), str(uuid4()), first_name, last_name, is_seller, is_admin, is_mod])

while True:
    TODO = input(">> ")

    if TODO == 'q':
        break

    if TODO == 'c':
        createUser()
