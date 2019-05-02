import os
import psycopg2


from app.version1.utilities.db.tables import queries, droppings
from werkzeug.security import generate_password_hash

def dbconnection():
    """making a connection to the db"""
    url = os.getenv('DATABASE_URL')
    return psycopg2.connect(url)


def initializedb():
    try:
        """starting the database"""
        connection = dbconnection()
        connection.autocommit = True

        """activate cursor"""
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query)
        connection.commit()

        """Generate the default admin and add to db"""
        gen_admin = """
                INSERT INTO
                users (firstname, lastname, email, password, isadmin)
                VALUES ('mainadmin', 'admin', 'admin12@gmail.com', '%s', true)
                ON CONFLICT (email) DO NOTHING;
                """%(generate_password_hash("passadmin"))
        connection = dbconnection()
        cursor = connection.cursor()
        cursor.execute(gen_admin)
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("DB Error")
        print(error)

def drop_tables():
    """Drops all tables"""
    connection = dbconnection()
    cursor = connection.cursor()
    for drop in droppings:
        cursor.execute(drop)
    connection.commit()