"""creating tables for the database"""
users_table = """CREATE TABLE IF NOT EXISTS users
            (
                user_id SERIAL PRIMARY KEY, 
                firstname VARCHAR(50) NOT NULL,
                lastname VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR (300) NOT NULL,
                registered TIMESTAMP DEFAULT NOW(),
                isadmin BOOLEAN DEFAULT FALSE
        )"""

queries = [users_table]
droppings = [
                "DROP TABLE users CASCADE"
            ]