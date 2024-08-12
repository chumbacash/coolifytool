import sqlite3

class User:
    def __init__(self, name, country, email, password):
        self.name = name
        self.country = country
        self.email = email
        self.password = password

    @staticmethod
    def create_user(name, country, email, password):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, country, email, password) VALUES (?, ?, ?, ?)",
                    (name, country, email, password))
        conn.commit()
        conn.close()
