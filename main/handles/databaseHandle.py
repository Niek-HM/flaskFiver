import sqlite3, pathlib
import atexit

class Create: # NOTE Create the database/tables
    def __init__(self):
        self.fileLoc = pathlib.Path(__file__).parent.resolve()

        self.connection = sqlite3.connect(f'{self.fileLoc}/../database/main.db') # NOTE Connect to the database
        self.cursor = self.connection.cursor() # NOTE Runs the commands like the cmd/terminal

        self.database_exists() # NOTE Create the database
        self.connection.close() # NOTE Close connection

    def database_exists(self):
        with open(f'{self.fileLoc}/../sql/create_tables.sql', 'r') as f: sqlData = f.read() # NOTE read sql file
        self.cursor.executescript(sqlData) # NOTE Execute the sql script
        self.connection.commit() # NOTE Save the database

class ReadWrite: # NOTE Make it possible to read/write from the database
    def __init__(self):
        self.fileLoc = pathlib.Path(__file__).parent.resolve()

        self.connection = sqlite3.connect(f'{self.fileLoc}/../database/main.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

        atexit.register(self.exit_handler) # NOTE Makes sure that the database is correctly closed

    def read(self, tables, rows, specification=''): # NOTE Read from database
        self.cursor.execute(f'SELECT {rows} FROM {tables} {specification}')
        rows = self.cursor.fetchall()

        return rows

    def write(self, table, columns, values, specification=''): # NOTE Write to database
        input_ = '?'

        for _ in range(values.__len__()-1): input_ += ', ?'

        self.cursor.execute(f'INSERT INTO {table}({columns}) VALUES({input_});', values) # NOTE Write to the database
        
        if self.cursor.rowcount == 1:
            self.connection.commit() # NOTE Commit changes
            return True
        else: return False # Return false if the commit was not successfull

    def changeData(self, table: str, columns: list, values: list, specification=''): # NOTE Change data in the database
        for i in range(columns.__len__()): self.cursor.execute(f'UPDATE {table} SET {str(columns[i-1])}="{str(values[i-1])}" {specification};') # NOTE Change data 
        
        if self.cursor.rowcount >= 1:
            self.connection.commit()
            return True
        else: return False

    def exit_handler(self):
        self.connection.close() # NOTE Close the connection