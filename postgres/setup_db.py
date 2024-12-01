import psycopg2

from config import db_config


def create_tables():
    commands = (
        """
        DROP TABLE IF EXISTS tasks;
        """,
        """
        DROP TABLE IF EXISTS users;
        """,
        """
        DROP TABLE IF EXISTS status;
        """,
        """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100),
            email VARCHAR(100) UNIQUE
        );
        """,
        """
        CREATE TABLE status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE
        );
        """,
        """
        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            description TEXT,
            status_id INTEGER REFERENCES status(id),
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )

    conn = psycopg2.connect(**db_config)

    try:
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)

        conn.commit()

        cur.close()
        print("tables created successfully")
    except Exception as error:
        print(f"unable to create tables: {error}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_tables()
