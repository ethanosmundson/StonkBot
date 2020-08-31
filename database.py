import sqlite3
from sqlite3 import *

conn = None

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
        print('SQLite version ' + str(sqlite3.version))
    except Error as e:
        print(e)
    
    
def end_connection():
    if conn:
        conn.close()

def execute_command(conn, command):
    try:
        c = conn.cursor()
        c.execute(command)
        conn.commit()
    except Error as e:
        print(e)
        if e.args[0].startswith('UNIQUE constraint'):
            raise RuntimeError('Watchlist already exists.') # catch this later
