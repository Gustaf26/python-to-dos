"""To-do list where you can add your tasks, modify them and delete if they have been completed.
  A cleanup feature enables you to delete completed tasks"""

"""I follow SQL syntax for queries, available at https://www.tutorialspoint.com/sql/sql-delete-query.htm"""

from collections import OrderedDict
import random
import datetime
import os
import modify

import sqlite3

# sqlite3.connect is the connection object to the database
con = sqlite3.connect('to_do_list.db')
# Con.cursor() is an inner object that gives us access to SQL Queries
cur = con.cursor()

class ToDo():
    """Model for creating to-do items. 'done' indicates that it's been completed,
    'protected' makes it immune to cleanup"""
    #task = str
    timestamp = datetime.datetime.today() + datetime.timedelta(hours=12)
    #done = False
    #protected = False

    class Meta:
         database = con


def clear():
    """Clear the display"""
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Connect to database"""
    con

# Function to view todos
def view_entries(entries):

    """"View to-do list"""
    clear()
    for row in entries:
        print(row)

    print('\nMY TO-DO LIST')
    print('=' * 40)
    return entries  

# Function to add a new to do
def add_entry(entries):
    """Add a new task"""

    new_task = input('\nTo do: ')
    protect = 'No'
    tasklimit = str(ToDo.timestamp)
    taskinfo = (new_task, 'undone', protect, random.randint(0,10000000), tasklimit)
    cur.execute("INSERT INTO mytodos VALUES(?,?,?,?,?)" , taskinfo)
    entries = cur.execute('SELECT * FROM mytodos')
    view_entries(entries)

# Function to modify an existing to do taken by id
def modify_entry(entries):
    """Modify selected entry"""
    id = input('Enter id of task')
    print('\n\n')

    # Loop through submenu to see what we wanna do with the to do
    for key, value in sub_menu.items():
        print('{}) {}'.format(key, sub_menu[key].__doc__))
    print('q) Back to Main')
    next_action = input('Action: ')

    # Action to be taken, each action imported from modify.py
    if next_action.lower().strip() in sub_menu:
        sub_menu[next_action](cur, id)
        entries = cur.execute('SELECT * FROM mytodos')
        view_entries(entries)
    else:
        return


def cleanup_entries(entries):
    """Cleanup: delete of entries with status 'Done'"""
    if (input('Are you sure you want to delete the done tasks? [yN]').lower().strip() == 'y'):
        entries = cur.execute('SELECT * FROM mytodos')
        for entry in entries:
            if "Done" in entry:
                print('hello')
                cur.execute(f"DELETE FROM mytodos WHERE DONE = 'Done'")
        entries = cur.execute('SELECT * FROM mytodos')
        view_entries(entries)


def menu_loop():
    choice = None
    entries = cur.execute('SELECT * FROM mytodos')
    view_entries(entries)
    while choice != 'q':
        if entries:
            print('\n' + '=' * 40 + '\n')

        #The items() method returns a view object. 
        # The view object contains the key-value pairs of the dictionary, 
        # as tuples in a list.
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        print('q) Quit')

        choice = input('\nAction: ')
        if choice in main_menu:
            try:
                main_menu[choice](entries)
            except ZeroDivisionError:
                continue

# An OrderedDict is a dictionary that remembers the order that keys were first inserted. 
# The only difference between dict() and OrderedDict() is that:
# OrderedDict preserves the order in which the keys are inserted. 
# A regular dict doesn’t track the insertion order, and iterating it gives 
# the values in an arbitrary order. By contrast, the order the items are 
# inserted is remembered by OrderedDict.

main_menu = OrderedDict([
    ('a', add_entry),
    ('m', modify_entry),
    ('c', cleanup_entries)
])

sub_menu = OrderedDict([
    ('m', modify.modify_task),
    ('d', modify.toggle_done),
    ('e', modify.delete_entry)
])

if __name__ == '__main__':
    initialize()
    menu_loop()
    cur.close()
