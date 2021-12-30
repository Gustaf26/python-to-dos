"""To-do list where you can chronologically add your tasks, modify them and mark if they have been completed.
  A cleanup feature enables you to delete completed tasks which are more than a week old - unless
  you have flagged them as 'protected'."""
from collections import OrderedDict
import random
import datetime
import os
import modify

import sqlite3
con = sqlite3.connect('to_do_list.db')
con.isolation_level = None
cur = con.cursor()

# from peewee import *


class ToDo():
    """Model for creating to-do items. 'done' indicates that it's been completed,
    'protected' makes it immune to cleanup"""
    task = str
    timestamp = datetime.datetime.today()
    done = False
    protected = False

    class Meta:
        database = con


def clear():
    """Clear the display"""
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Connect to database"""
    con


def view_entries(index, entries, single_entry):

    """"View to-do list"""
    clear()
    for row in entries:
        print(row)

    # determines which entry is selected for modification
    # if single_entry:  # to see only 1 entry
    #     entries = [entries[index]]
    #     index = 0
    # else:
    print('\nMY TO-DO LIST')
    print('=' * 40)

    return entries  # so that we can modify the given entry if needed


def add_entry(entries):
    """Add a new task"""

    new_task = input('\nTo do: ')
    if input('Protect [yN]? ').lower().strip() == 'y':
        protect = True
    else:
        protect = False

    tasklimit = str(ToDo.timestamp)
    taskinfo = (new_task, 'undone', protect, random.randint(0,10000000), tasklimit)
    cur.execute("INSERT INTO mytodos VALUES(?,?,?,?,?)" , taskinfo)
    entries = cur.execute('SELECT * FROM mytodos')
    view_entries(0, entries, False)


def modify_entry(entries):
    """Modify selected entry"""
    id = input('Enter id of task')
    print('\n\n')

    for key, value in sub_menu.items():
        print('{}) {}'.format(key, sub_menu[key].__doc__))
    print('q) Back to Main')
    next_action = input('Action: ')

    if next_action.lower().strip() in sub_menu:
        sub_menu[next_action](cur, id)
        entries = cur.execute('SELECT * FROM mytodos')
        view_entries(0,entries,False)
    else:
        return


def cleanup_entries(entries):
    """Cleanup: delete completed, non-protected entries older than a week"""
    if (input('Are you sure you want to delete the done tasks? [yN]').lower().strip() == 'y'):
        for entry in entries:
            if "done" in entry:
                cur.execute(f'DELETE FROM mytodos WHERE DONE = "Done"')
        view_entries(0,entries, False)


def menu_loop():
    choice = None
    index = 0  # shows which entry is selected
    entries = cur.execute('SELECT * FROM mytodos')
    view_entries(index, entries, False)
    while choice != 'q':
        if entries:
            print('\n' + '=' * 40 + '\n')
        for key, value in main_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        print('q) Quit')

        choice = input('\nAction: ')
        if choice in main_menu:
            try:
                main_menu[choice](entries)
            except ZeroDivisionError:
                continue

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
