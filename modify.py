# These are the modification options for the chosen to-do that is going to be modified

# They all take the todo-id -that you set into the terminal when running the program- as argument and receive as first argument the cur object that lets us modify the db

# They also have for-loops, which loop through the entries in db in order to do something with the specified entry (toggle done, modify task or delete)

# Let´s modify a task!
def modify_task(cur, id):
    """Modify task"""
    new_task = input('Change task to something else > ')
    entries = cur.execute('SELECT * FROM mytodos')
    for entry in entries:
        if int(id) in entry:
            cur.execute(f"UPDATE mytodos SET TASK='{str(new_task)}' WHERE ID={id}")

# Obviously this function will set a chosen to-do to Done or undone in your db
def toggle_done(cur, id):
    """Toggle 'DONE'"""
    entries = cur.execute('SELECT * FROM mytodos')
    for entry in entries:
        if int(id) in entry and 'undone' in entry:
            cur.execute(f"UPDATE mytodos SET DONE='Done' WHERE ID={id}")
        elif int(id) in entry and 'Done' in entry:
            cur.execute(f"UPDATE mytodos SET DONE='undone' WHERE ID={id}")

# And this rascal will take the to-do you want to kill and just erase it
# from SQLite
def delete_entry(cur, id):
    """Erase entry"""
    if (input('Are you sure [yN]? ').lower().strip() == 'y'):
        entries = cur.execute('SELECT * FROM mytodos')
        for entry in entries:
            if int(id) in entry:
                cur.execute(f"DELETE FROM mytodos WHERE ID={id}")