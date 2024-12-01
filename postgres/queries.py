import psycopg2

from config import db_config


def execute_query(query, params=None):
    conn = psycopg2.connect(**db_config)

    try:
        cur = conn.cursor()
        cur.execute(query, params)
        if query.strip().upper().startswith('SELECT'):
            records = cur.fetchall()
            for row in records:
                print(row)
        else:
            conn.commit()
            print("query executed successfully")
        cur.close()
    except Exception as error:
        print(f"unable to execute query: {error}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    print("Get all tasks of a certain user")
    user_id = 1
    query1 = "SELECT * FROM tasks WHERE user_id = %s;"
    execute_query(query1, (user_id,))
    print()

    print("Select tasks by a certain status")
    status_name = 'new'
    query2 = """
    SELECT * FROM tasks WHERE status_id = (
        SELECT id FROM status WHERE name = %s
    );
    """
    execute_query(query2, (status_name,))
    print()

    print("Update the status of a specific task")
    task_id = 2
    new_status_name = 'in progress'
    query3 = """
    UPDATE tasks SET status_id = (
        SELECT id FROM status WHERE name = %s
    ) WHERE id = %s;
    """
    execute_query(query3, (new_status_name, task_id))
    print()

    print("Get a list of users who do not have any tasks")
    query4 = """
    SELECT * FROM users WHERE id NOT IN (
        SELECT DISTINCT user_id FROM tasks
    );
    """
    execute_query(query4)
    print()

    print("Add a new task for a specific user")
    user_id = 3
    title = 'New Task Title'
    description = 'This is a new task description.'
    status_name = 'new'
    query5 = """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s);
    """
    execute_query(query5, (title, description, status_name, user_id))
    print()

    print("Get all tasks that are not yet completed")
    query6 = """
    SELECT * FROM tasks WHERE status_id != (
        SELECT id FROM status WHERE name = 'completed'
    );
    """
    execute_query(query6)
    print()

    print("Delete a specific task")
    task_id = 4
    query7 = "DELETE FROM tasks WHERE id = %s;"
    execute_query(query7, (task_id,))
    print()

    print("Find users with a specific email")
    email_pattern = '%@example.com'
    query8 = "SELECT * FROM users WHERE email LIKE %s;"
    execute_query(query8, (email_pattern,))
    print()

    print("Update the name of a user")
    user_id = 5
    new_fullname = 'Malcolm Shade'
    query9 = "UPDATE users SET fullname = %s WHERE id = %s;"
    execute_query(query9, (new_fullname, user_id))
    print()

    print("Get the number of tasks for each status")
    query10 = """
    SELECT s.name, COUNT(t.id) FROM status s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.name;
    """
    execute_query(query10)
    print()

    print("Get tasks assigned to users with a certain email domain")
    email_domain = '%@example.com'
    query11 = """
    SELECT t.* FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE %s;
    """
    execute_query(query11, (email_domain,))
    print()

    print("Get a list of tasks that do not have a description")
    query12 = "SELECT * FROM tasks WHERE description IS NULL OR description = '';"
    execute_query(query12)
    print()

    print("Select users and their tasks that are in the 'in progress' status")
    query13 = """
    SELECT u.fullname, t.title FROM users u
    JOIN tasks t ON u.id = t.user_id
    JOIN status s ON t.status_id = s.id
    WHERE s.name = 'in progress';
    """
    execute_query(query13)
    print()

    print("Get users and the number of their tasks")
    query14 = """
    SELECT u.fullname, COUNT(t.id) FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.fullname;
    """
    execute_query(query14)
    print()
