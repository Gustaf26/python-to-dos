def modify_task(cur, id):
    """Modify task"""
    new_task = input('Change task to something else > ')
    entries = cur.execute('SELECT * FROM mytodos')
    for entry in entries:
        if int(id) in entry:
            cur.execute(f"UPDATE mytodos SET TASK='{str(new_task)}' WHERE ID={id}")

def toggle_done(cur, id):
    """Toggle 'DONE'"""
    entries = cur.execute('SELECT * FROM mytodos')
    for entry in entries:
        if int(id) in entry and 'undone' in entry:
            cur.execute(f"UPDATE mytodos SET DONE='Done' WHERE ID={id}")
        elif int(id) in entry and 'Done' in entry:
            cur.execute(f"UPDATE mytodos SET DONE='undone' WHERE ID={id}")