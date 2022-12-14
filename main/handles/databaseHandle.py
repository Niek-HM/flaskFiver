import sqlite3, pathlib
import atexit

class Create: #* Create the database
    def __init__(self):
        self.fileLoc = pathlib.Path(__file__).parent.resolve()

        self.connection = sqlite3.connect(f'{self.fileLoc}/../database/main.db') # Connect to the database
        self.cursor = self.connection.cursor() # Can run commands like a cmd

        self.database_exists()
        self.connection.close() # Close connection

    def database_exists(self):
        with open(f'{self.fileLoc}/../sql/create_tables.sql', 'r') as f: sqlData = f.read()
        self.cursor.executescript(sqlData) # Execute a script
        self.connection.commit() # Save the database

class ReadWrite: #* Read or write to the database
    def __init__(self):
        self.fileLoc = pathlib.Path(__file__).parent.resolve()

        self.connection = sqlite3.connect(f'{self.fileLoc}/../database/main.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

        atexit.register(self.exit_handler)

    def read(self, tables, rows, specification=''):
        self.cursor.execute(f'SELECT {rows} FROM {tables} {specification}')
        rows = self.cursor.fetchall()

        return rows

    def customRead(self, command): #! Never use this if it is not needed
        self.cursor.execute(command)
        rows = self.cursor.fetchall()

        return rows #! Make sure you pop the values you don't need

    def write(self, table, columns, values, specification=''):
        input_ = '?'

        for i in range(values.__len__()-1): input_ += ', ?'

        self.cursor.execute(f'INSERT INTO {table}({columns}) VALUES({input_});', values)
        if self.cursor.rowcount == 1:
            self.connection.commit()
            return True
        else: return False # Returns if commit was not successfull

    def changeData(self, table, columns, values, specification=''):
        for i in range(columns.__len__()):
            self.cursor.execute(f'UPDATE {table} SET {str(columns[i-1])}="{str(values[i-1])}" {specification};')
        
        if self.cursor.rowcount >= 1:
            self.connection.commit()
            return True
        else: return False

    def exit_handler(self):
        self.connection.close()