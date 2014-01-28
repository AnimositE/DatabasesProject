import urlparse
import psycopg2
import os

class Database:

    conn = False
    cursor = False

    def __init__(self):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        cursor = conn.cursor()

    def getDivers(self):
        cursor.execute("SELECT * FROM Divers;")
        return cursor.fetchall()

    def getMeets(self):
        cursor.execute("SELECT * FROM Meets;")
        return cursor.fetchall()

    def getDives(self):
        cursor.execute("SELECT * FROM Dives;")
        return cursor.fetchall()

    def login(self, email, password):
    	cursor.execute("SELECT * FROM Divers \
    						WHERE email=%s AND hashpass=%s;",[email,password])
    	return cursor.fetchall()