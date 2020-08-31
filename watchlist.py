import sqlite3
from sqlite3 import Error
import database as db

conn = db.create_connection(r'watchlist.db') # connects to database for watchlists

# creates a table to store data
db.execute_command(conn, '''CREATE TABLE IF NOT EXISTS watchlist (
                                user_id int,
                                watchlist_name varchar(255),
                                symbols varchar(255),
                                unique (user_id, watchlist_name)
                            );''')

def create_watchlist(user_id, watchlist_name):
    '''Creates a watchlist for a user'''
    try:
        db.execute_command(conn, f'''INSERT INTO watchlist(user_id, watchlist_name) VALUES ({user_id}, '{watchlist_name}')''')
        return 'Success embed'
    except RuntimeError:
        return 'Watchlist already exists!'

def remove_watchlist(user_id, watchlist_name):
    '''Deletes an existing watchlist'''
    # will search for the entry in the database with user id, and watchlist name if found removes else returns an error embed
    return

def add_symbol(user_id, symbol, watchlist_name):
    '''Adds a symbol passed in, to a watchlist'''
    # adds symbol to the 'symbols' field of the database for the user id and watchlist name
    return

def remove_symbol(user_id, symbol, watchlist_name):
    '''Removes symbol from a specific watchlist'''
    # removes symbol to the 'symbols' field of the database for the user id and watchlist name. If not found return an error
    return

def display_watchlist(user_id, watchlist_name):
    '''Returns an embed containing name of watchlist, open, and current price data for each stock on their watchlist'''
    #TODO: make helper function in finnhub.py for this 
    return

def display_user_watchlists(user_id):
    '''Returns an embed containing a list of all watchlists created by a user.'''
    return

create_watchlist(19341924924, 'heahah')
# def main_test():
#     create_watchlist()

# if __name__ == '__main__':
#     main_test()