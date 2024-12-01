import psycopg2
from faker import Faker

from config import db_config


def seed_status_table(cur):
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))


def seed_users_table(cur, fake, num_users=10):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s);", (fullname, email))


def seed_tasks_table(cur, fake, num_tasks=50):
    cur.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cur.fetchall()]

    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        if fake.random_int(min=1, max=100) <= 90:
            description = fake.paragraph(nb_sentences=3)
        else:
            description = None
        status_id = fake.random_element(elements=status_ids)
        user_id = fake.random_element(elements=user_ids)
        cur.execute("""
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s);
            """, (title, description, status_id, user_id))


def main():
    fake = Faker()

    conn = psycopg2.connect(**db_config)

    try:
        cur = conn.cursor()

        seed_status_table(cur)
        seed_users_table(cur, fake)
        seed_tasks_table(cur, fake)

        conn.commit()
        cur.close()
        print("data seeded successfully")
    except Exception as error:
        print(f"unable to seed data: {error}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
